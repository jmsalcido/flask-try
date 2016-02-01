module.exports = function (grunt) {

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        watch: {
            scripts: {
                files: ['assets/**/*'],
                tasks: ['package-dev'],
                options: {
                    spawn: false
                }
            }
        },
        clean: [
            "dist",
            "app/static/js/",
            "app/static/css/",
            "app/static/fonts/"
        ],
        copy: {
            main: {
                files: [
                    {
                        expand:true,
                        cwd: "assets/",
                        src: [
                            'js/*.min.js',
                            'css/*.min.css',
                            'fonts/*'
                        ],
                        dest: 'app/static/',
                        filter: 'isFile'
                    },
                    {
                        expand: true,
                        cwd: 'dist/',
                        src: [
                            'js/*.min.js',
                            'css/*.min.css',
                            'fonts/*'
                        ],
                        dest: 'app/static/',
                        filter: 'isFile'
                    }
                ]
            },
            dev: {
                files: [
                    {
                        expand:true,
                        cwd: "assets/",
                        src: [
                            'js/*.js',
                            'css/*.css',
                            'fonts/*'
                        ],
                        dest: 'app/static/',
                        filter: 'isFile'
                    },
                    {
                        expand: true,
                        cwd: 'dist/',
                        src: [
                            'js/*.js',
                            'css/*.css',
                            'fonts/*'
                        ],
                        dest: 'app/static/',
                        filter: 'isFile'
                    }
                ]
            }
        },
        uglify: {
            options: {
                banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
            },
            build: {
                files: [{
                    expand: true,
                    flatten: true,
                    src: ['dist/js/*.js', 'assets/js/*.js'],
                    dest: 'dist/js/',
                    ext: '.min.js'
                }]
            }
        },
        bowercopy: {
            options: {
                scrPrefix: 'bower_components'
            },
            scripts: {
                options: {
                    destPrefix: 'dist/'
                },
                files: {
                    "js/jquery.js": "jquery/dist/jquery.js",
                    "js/bootstrap.js": "bootstrap/dist/js/bootstrap.js",
                    "css/bootstrap.css": "bootstrap/dist/css/bootstrap.css",
                    "js/moment.js": "moment/moment.js"
                }
            },
            folders: {
                options: {
                    destPrefix: 'dist/'
                },
                files: {
                    "fonts": "bootstrap/dist/fonts"
                }
            }
        }
    });

    // Load the plugin that provides the "uglify" task.
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-bowercopy');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-watch');

    // Default task(s).
    grunt.registerTask('default', ['clean']);
    grunt.registerTask('package-dev', ['clean', 'bowercopy', 'copy:dev']);
    grunt.registerTask('package', ['clean', 'bowercopy', 'uglify', 'copy:main']);

};