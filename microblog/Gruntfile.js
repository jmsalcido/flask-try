module.exports = function (grunt) {

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        clean: [
            "dist",
            "app/static/js/"
        ],
        copy: {
            main: {
                files: [
                    {
                        expand:true,
                        flatten: true,
                        src: ['dist/js/*.min.js'],
                        dest: 'app/static/js/',
                        filter: 'isFile'
                    }
                ]
            },
            dev: {
                files: [
                    {
                        expand:true,
                        flatten: true,
                        src: ['dist/js/*.js'],
                        dest: 'app/static/js/',
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
                    src: 'dist/js/*.js',
                    dest: 'dist/js/ugly/',
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
                    destPrefix: 'dist/js/'
                },
                files: {
                    "jquery.js": "jquery/src/jquery.js",
                    "bootstrap.js": "bootstrap/dist/js/bootstrap.js"
                }
            }
        }
    });

    // Load the plugin that provides the "uglify" task.
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-bowercopy');
    grunt.loadNpmTasks('grunt-contrib-clean');

    // Default task(s).
    grunt.registerTask('default', ['clean']);
    grunt.registerTask('package-dev', ['clean', 'bowercopy', 'copy:dev']);
    grunt.registerTask('package', ['clean', 'bowercopy', 'uglify', 'copy']);

};