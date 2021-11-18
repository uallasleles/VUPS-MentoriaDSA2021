var gulp            = require('gulp');
var browserSync     = require('browser-sync').create();     // adiciona prefixos de fornecedor ao CSS como  -webkit- , -ms- , etc.
// var autoprefixer = require('gulp-autoprefixer');
var del             = require('del');
var sass            = require('gulp-sass')(require('node-sass'));
var cleanCss        = require('gulp-clean-css');
const cssbeautify   = require('gulp-cssbeautify');
var concat          = require('gulp-concat');
var terser          = require('gulp-terser');
const htmlmin       = require('gulp-htmlmin');
const npmDist       = require('gulp-npm-dist');     // listar as dependências do package.json e copiar os arquivos dist deles para uma pasta específica
var wait            = require('gulp-wait');                        
var sourcemaps      = require('gulp-sourcemaps');   // indica se um mapa de origem para o arquivo empacotado deve ser gerado ou não. O valor padrão é falso.
                                                    // mapeia os estilos CSS de volta ao arquivo SCSS original nas ferramentas de desenvolvimento do seu navegador
var fileinclude     = require('gulp-file-include');
var rename          = require("gulp-rename");

// Definir caminhos
const paths = {
    dist: { // distribution
        base:   './dist/',
        css:    './dist/css',
        js:     './dist/js',
        html:   './dist/pages',
        assets: './dist/assets',
        img:    './dist/assets/img',
        vendor: './dist/vendor'
    },
    dev: { // developement
        base:   './html&css/',
        css:    './html&css/css',
        html:   './html&css/pages',
        assets: './html&css/assets',
        img:    './html&css/assets/img',
        vendor: './html&css/vendor'
    },
    base: {
        base: './',
        node: './node_modules'
    },
    src: { // source
        base:           './',
        css:            './css',
        js:             './js',
        html:           './src/pages/**/*.html',
        assets:         './src/assets/**/*.*',
        partials:       './src/partials/**/*.html',
        scss:           './scss',
        node_modules:   './node_modules/',
        vendor:         './vendor'
    },
    temp: {
        base:   './.temp/',
        css:    './.temp/css',
        js:    './.temp/js',
        html:   './.temp/pages',
        assets: './.temp/assets',
        vendor: './.temp/vendor'
    }
};

// Tarefa padrão
function defaultTask(cb) {
    // coloque o código para sua tarefa padrão aqui
    cb();
};
exports.defaultTask = defaultTask;

// Copiar arquivos
function copy(cp){
    gulp.src(paths.src.js + '/*.js')
    .pipe(gulp.dest(paths.dist.js));
    cp();
};
exports.copy = copy;

// Compilar SASS
gulp.task('scss', function() {
    return gulp.src([
        paths.src.scss + '/custom/**/*.scss', 
        paths.src.scss + '/volt/**/*.scss', 
        paths.src.scss + '/volt.scss'])
        .pipe(wait(500))
        .pipe(sourcemaps.init())
        .pipe(sass().on('error', sass.logError))
        .pipe(sourcemaps.write('../css'))
        .pipe(gulp.dest(paths.src.css))
        .pipe(browserSync.stream()); // injetar alterações sem atualizar a página
        // isso é usado em CSS e outros formatos de folha de estilo
        // é útil porque mantém a posição de rolagem intacta 
        // e não leva você para o topo da página como uma atualização de página normalmente faria
});

// Minificar CSS
gulp.task('minify:css', function() {
    return gulp.src([
            paths.src.css + '/volt.css'
        ])
        .pipe(cleanCss())
        .pipe(rename(function(path) {
            // Updates the object in-place
            path.basename = "style";
            path.extname = ".min.css";
        }))
        .pipe(gulp.dest(paths.dist.css))
});

// Minificar JS
gulp.task('minify:js', function() {
    return gulp.src([
            paths.src.js + '/*.js'
        ])
        .pipe(concat('all.js'))
        .pipe(terser())
        .pipe(rename(function(path) {
            // Updates the object in-place
            path.extname = ".min.js";
        }))
        .pipe(gulp.dest(paths.dist.js))
});

// Minificar HTML
gulp.task('minify:html', function() {
    return gulp.src([
        paths.src.html + "/*.html"])
        .pipe(wait(500))
        .pipe(htmlmin({collapseWhitespace: true}))
        .pipe(gulp.dest(paths.dist.html))
})

gulp.task('copy:libs', function() {
    return gulp.src(
        npmDist(), {base:'./node_modules/'})
        .pipe(sourcemaps.init())
        .pipe(rename(function(path) {
            path.dirname = path.dirname.replace(/\/dist/, '').replace(/\\dist/, '');
        }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(paths.dist.vendor));
});

// Build
gulp.task('build', gulp.series('scss', 'minify:css', 'minify:js', 'minify:html', 'copy:libs'));
