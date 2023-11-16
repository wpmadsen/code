// Gulpfile for WebDev projects
//
// See README for details.
//
// ==============================================================================
//
// CUSTOMIZATION NOTES
//
// If you modify this file, it's recommended that you put comments around your
// changes with "CUSTOM" and an explanation. This'll make it much easier to
// upgrade your app to newer build processes later on.
//
// ==============================================================================

const { src, dest, lastRun, series, parallel, watch } = require('gulp');
const { spawn } = require('child_process');
const debug = require('gulp-debug');
const del = require('del');
const merge = require('merge2');
const path = require('path');
const ignore = require('gulp-ignore');

// ----------------------------------------------------------------------------
// CSS requirements

const sass = require('gulp-sass')(require('sass'));
const autoprefixer = require('gulp-autoprefixer');
const cssnano = require('gulp-cssnano');

// ----------------------------------------------------------------------------
// JavaScript requirements

const babel = require('gulp-babel');
const uglify = require('gulp-uglify');



// ----------------------------------------------------------------------------
// Configuration

const BASE_ASSET_PATH = '../assets';
const CSS_ASSET_PATH = BASE_ASSET_PATH + '/css/**/*.+(scss|css)';
const JS_ASSET_PATH = BASE_ASSET_PATH + '/js/**/*.js';

const BASE_OUTPUT_PATH = '../libcal_bookings/static';
const CSS_OUTPUT_PATH = BASE_OUTPUT_PATH + '/css/';
const JS_OUTPUT_PATH = BASE_OUTPUT_PATH + '/js/';

// Files to copy
const filesToCopy = [
    // Images
    {
        src: BASE_ASSET_PATH + '/img/**/*',
        dest: BASE_OUTPUT_PATH + '/img/',
    },

    // JS libraries
    {
        src: BASE_ASSET_PATH + '/js/lib/**/*',
        dest: BASE_OUTPUT_PATH + '/js/lib/',
    },

    // CSS libraries
    {
        src: BASE_ASSET_PATH + '/css/lib/**/*',
        dest: BASE_OUTPUT_PATH + '/css/lib/',
    },

    // etc.
];


// ----------------------------------------------------------------------------
// Clean

function clean(cb) {
    // Deletes everything in BASE_OUTPUT_PATH (usually libcal_bookings/static)
    del.sync([BASE_OUTPUT_PATH], { 'force': true });

    cb();
}



// ----------------------------------------------------------------------------
// CSS

function css() {
    // This task currently does SASS conversion and autoprefixing
    return src(CSS_ASSET_PATH, { sourcemaps: true })
        // Ignore libraries (we use this instead of ! in the src because the
        // latter doesn't work as advertised. I spent many hours trying to get
        // it working. I hate it.
        .pipe(ignore('lib/**/*'))

        // DEBUG (if you need to see what files are getting processed,
        // uncomment this line)
        // .pipe(debug())

        // Convert SCSS to CSS
        .pipe(sass())
        // Autoprefix CSS
        .pipe(autoprefixer({
            overrideBrowserslist: ['last 2 versions'],
            cascade: false
        }))
        // Minify CSS
        .pipe(cssnano())
        // And save to disk
        .pipe(dest(CSS_OUTPUT_PATH, { sourcemaps: '.' }));
}

function cssWatch() {
    // This task watches the CSS asset path and runs the css task when changes
    // are made to the files
    return watch(CSS_ASSET_PATH, css);
}



// ----------------------------------------------------------------------------
// JavaScript

function js() {
    // This task currently does Babel transpiling
    return src(JS_ASSET_PATH, { sourcemaps: true })
        // Ignore libraries and minified files
        .pipe(ignore('lib/**/*'))

        // DEBUG (if you need to see what files are getting processed,
        // uncomment this line)
        // .pipe(debug())

        // Transpile via Babel
        .pipe(babel({
            presets: ['@babel/env']
        }))
        // Minify
        .pipe(uglify())
        // And save the JS to disk
        .pipe(dest(JS_OUTPUT_PATH, { sourcemaps: '.' }));
}

function jsWatch() {
    // This task watches the JS asset path and runs the js task when changes
    // are made to the files
    return watch(JS_ASSET_PATH, js);
}



// ----------------------------------------------------------------------------
// Copying

// Copy static files
function copy(cb) {
    // Go through each entry in filesToCopy
    filesToCopy.map(({ src: srcPath, dest: destFile }) => {
        // Delete anything in the dest (force lets it delete files outside the
        // current working directory)
        del.sync([destFile], { force: true });

        // And copy the files over
        return src(srcPath)
            // DEBUG (if you need to see what files are getting processed,
            // uncomment this line)
            // .pipe(debug())

            .pipe(dest(destFile));
    });

    cb();
}

function copyWatch(cb) {
    // Go through each entry in filesToCopy
    filesToCopy.map(({ src: srcPath, dest: destPath }) => {
        // --------------------------
        // This part should be the same as inside copy()

        // DEBUG (if you need to see what files are getting processed,
        // uncomment this line)
        // console.log(srcPath + " -> " + destFile);

        // Delete anything in the dest (force lets it delete files outside the
        // current working directory)
        // del.sync([destPath], { force: true });

        // And copy the files over
        src(srcPath)
            // DEBUG (if you need to see what files are getting processed,
            // uncomment this line)
            // .pipe(debug())

            .pipe(dest(destPath));

        // --------------------------

        // Now start watching the srcPath
        watch(srcPath).on(
            'all',
            (event, srcPath) => {
                // DEBUG (if you need to see what files are getting processed,
                // uncomment this line)
                // console.log(event, srcPath);

                let destFile = path.join(destPath, path.basename(srcPath));

                // Process the watch event for this file
                if (event === 'add' || event === 'change') {
                    // File added/changed, so copy it from src to dest
                    src(srcPath)
                        .pipe(dest(destPath));
                } else if (event === 'unlink') {
                    // Delete the destination file since it was removed in src
                    del(destFile, { 'force': true });
                }
            }
        )
    });

    cb();
}



// ----------------------------------------------------------------------------
// Exports

exports.build = series(clean, parallel(js, css, copy));
exports.watch = series(exports.build, parallel(jsWatch, cssWatch, copyWatch));
exports.clean = clean;
exports.css = css;
exports.cssWatch = cssWatch;
exports.js = js;
exports.jsWatch = jsWatch;
exports.copy = copy;
exports.copyWatch = copyWatch;

exports.default = exports.watch;
