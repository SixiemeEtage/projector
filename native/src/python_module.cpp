#define PY_ARRAY_UNIQUE_SYMBOL pbcvt_ARRAY_API

#include <iostream>
#include <boost/python.hpp>
#include <pyboostcvconverter/pyboostcvconverter.hpp>

namespace libprojector {

    using namespace boost::python;

    std::ostream& operator<<(std::ostream& os, const boost::python::object& o) {
        return os << boost::python::extract<std::string>(boost::python::str(o))();
    }

    struct Ray {
        double x;
        double y;
        double z;
    };

    struct TexCoords {
        double u;
        double v;
    };

    class Projection {
    public:
        // Empty virtual destructor for proper cleanup
        virtual ~Projection() {}

        virtual int getWidth() const = 0;
        virtual int getHeight() const = 0;
        virtual void toRay(double u, double v, Ray& r) const = 0;
        virtual void toTexCoords(Ray r, TexCoords& point) const = 0;
    };

    typedef boost::shared_ptr<Projection> ProjectionPtr;

    class SphericalProjection: public Projection {
    private:
        double imageMidWidth;
        double imageMidHeight;
        double scale;

    public:
        SphericalProjection(int _imageWidth, int _imageHeight) : 
            imageMidWidth(static_cast<double>(_imageWidth)/2),
            imageMidHeight(static_cast<double>(_imageHeight)/2) {
                scale = imageMidWidth / M_PI;
            }

        int getWidth() const {
            return static_cast<int>(2 * imageMidWidth);
        }

        int getHeight() const {
            return static_cast<int>(2 * imageMidHeight);
        }

        void toRay(double u, double v, Ray& r) const {
            u -= imageMidWidth;
            v -= imageMidHeight;

            // ensure u-axis negative on the center left, positive on center right
            // ensure v-axis negative on the center bottom, positive on center top
            // u *= -1.0;
            v *= -1.0;

            u /= scale;
            v /= scale;

            double sinv = sinf(M_PI_2 - v);
            r.x = sinv * cosf(u);
            r.y = sinv * sinf(u);
            r.z = cosf(M_PI_2 - v);
        }

        void toTexCoords(Ray r, TexCoords& point) const {
            double u = scale * atan2f(r.x, r.z);
            double v = 0.0;
            double d = sqrtf(r.x * r.x + r.y * r.y + r.z * r.z);
            if (fabs(d) < DBL_EPSILON) {
                v = 0.0;
            } else {
                double w = r.y / d;
                v = scale * (M_PI - acosf(w));
            }

            point.u = u;
            point.v = v;
        }
    };

    /**
     Cubemap projection associated with the following cubemap layout
     
      --------
     |   +z   |
     |  side  |
      -------- -------- -------- -------- 
     |   -y   |   +x   |   +y   |   -x   |
     |  side  |  side  |  side  |  side  |
      -------- -------- -------- --------
     |   -z   |
     |  side  |
      --------

     */
    class CubemapProjection: public Projection {
    private:
        double sideWidth;
        double sideBorderPadding;  // can be used to give some pixels to the interpolation on the borders

    public:
        CubemapProjection(int _sideWidth, int _sideBorderPadding) : 
            sideWidth(static_cast<double>(_sideWidth)),
            sideBorderPadding(static_cast<double>(_sideBorderPadding)) {}

        int getWidth() const {
            return static_cast<int>(4 * sideWidth);
        }

        int getHeight() const {
            return static_cast<int>(3 * sideWidth);
        }

        void toRay(double u, double v, Ray& ray) const {
            
        }

        void toTexCoords(Ray r, TexCoords& point) const {
            double absX = fabs(r.x);
            double absY = fabs(r.y);
            double absZ = fabs(r.z);

            bool isXPositive = (r.x > 0);
            bool isYPositive = (r.y > 0);
            bool isZPositive = (r.z > 0);

            double maxAxis;
            double offsetXIndex, offsetYIndex;
            double u, v;

            // +x
            if (isXPositive && absX >= absY && absX >= absZ) {
                // u in [0,1] from -y to +y
                // v in [0,1] from +z to -z
                maxAxis = absX;
                offsetXIndex = 1;
                offsetYIndex = 1;
                u = r.y;
                v = -r.z;
            }
            // -x
            if (!isXPositive && absX >= absY && absX >= absZ) {
                // u in [0,1] from +y to +y
                // v in [0,1] from -z to +z
                maxAxis = absX;
                offsetXIndex = 3;
                offsetYIndex = 1;
                u = -r.y;
                v = -r.z;
            }

            // +y
            if (isYPositive && absY >= absX && absY >= absZ) {
                // u in [0,1] from +x to -x
                // v in [0,1] from +z to -z
                maxAxis = absY;
                offsetXIndex = 2;
                offsetYIndex = 1;
                u = -r.x;
                v = -r.z;
            }
            // -y
            if (!isYPositive && absY >= absX && absY >= absZ) {
                // u in [0,1] from -x to +x
                // v in [0,1] from +z to -z
                maxAxis = absY;
                offsetXIndex = 0;
                offsetYIndex = 1;
                u = r.x;
                v = -r.z;
            }

            // +z
            if (isZPositive && absZ >= absX && absZ >= absY) {
                // u in [0,1] from -x to +x
                // v in [0,1] from +y to -y
                maxAxis = absZ;
                offsetXIndex = 0;
                offsetYIndex = 0;
                u = r.x;
                v = -r.y;
            }
            // -z
            if (!isZPositive && absZ >= absX && absZ >= absY) {
                // u in [0,1] from -x to +x
                // v in [0,1] from -y to +y
                maxAxis = absZ;
                offsetXIndex = 0;
                offsetYIndex = 2;
                u = r.x;
                v = r.y;
            }

            // convert range from [-1,1] to [0,1]
            u = 0.5 * (u / maxAxis + 1.0);
            v = 0.5 * (v / maxAxis + 1.0);

            // convert the (u,v) to the layout described in the class comment (cross layout)
            point.u = offsetXIndex * sideWidth + sideBorderPadding + u * (sideWidth - 2*sideBorderPadding);
            point.v = offsetYIndex * sideWidth + sideBorderPadding + v * (sideWidth - 2*sideBorderPadding);
        }
    };

    typedef enum ProjectionType {
        ProjectionTypeSpherical,
        ProjectionTypeCubemap,
    } ProjectionType;

    class ProjectionConvertor {
    private:
        ProjectionPtr inProj;
        ProjectionPtr outProj;
        cv::Mat mapX;
        cv::Mat mapY;

    public:
        ProjectionConvertor(ProjectionPtr _inProj, ProjectionPtr _outProj) : 
            inProj(_inProj),
            outProj(_outProj) {}

        cv::Mat get_map_x() const { return mapX; }
        cv::Mat get_map_y() const { return mapY; }

        void convert() {
            int width = outProj->getWidth();
            int height = outProj->getHeight();

            mapX = cv::Mat(height, width, CV_32FC1);
            mapY = cv::Mat(height, width, CV_32FC1);

            for (int x = 0; x < width; ++x) {
                for (int y = 0; y < height; ++y) {
                    Ray r;
                    outProj->toRay(static_cast<double>(x), static_cast<double>(y), r);
                    // std::cout << "ray(x,y,z) = " << r.x << "," << r.y << "," << r.z << std::endl;

                    TexCoords t;
                    inProj->toTexCoords(r, t);
                    // std::cout << "tex(u,v) = " << t.u << "," << t.v << std::endl;

                    mapX.at<float>(y,x) = static_cast<float>(t.u);
                    mapY.at<float>(y,x) = static_cast<float>(t.v);
                }
            }
        }
    };


#if (PY_VERSION_HEX >= 0x03000000)
    static void *init_ar() {
#else
    static void init_ar(){
#endif
        Py_Initialize();

        import_array();
        return NUMPY_IMPORT_ARRAY_RETVAL;
    }

    BOOST_PYTHON_MODULE (libprojector) {
        //using namespace XM;
        init_ar();

        //initialize converters
        to_python_converter<cv::Mat, pbcvt::matToNDArrayBoostConverter>();
        pbcvt::matFromNDArrayBoostConverter();

        //expose module-level functions
        class_<SphericalProjection>("SphericalProjection", init<int, int>());
        class_<CubemapProjection>("CubemapProjection", init<int, int>());
        class_<ProjectionConvertor>("ProjectionConvertor", init<ProjectionPtr, ProjectionPtr>())
            .def("convert", &ProjectionConvertor::convert)
            .def("get_map_x", &ProjectionConvertor::get_map_x)
            .def("get_map_y", &ProjectionConvertor::get_map_y);

        implicitly_convertible<boost::shared_ptr<SphericalProjection>, ProjectionPtr>();
        implicitly_convertible<boost::shared_ptr<CubemapProjection>, ProjectionPtr>();
    }

} //end namespace libprojector
