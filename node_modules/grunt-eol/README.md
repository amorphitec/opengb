# grunt-eol

> Convert line endings the easy way.

## Getting Started
This plugin requires Grunt `~0.4.1`

If you haven't used [Grunt](http://gruntjs.com/) before, be sure to check out the [Getting Started](http://gruntjs.com/getting-started) guide, as it explains how to create a [Gruntfile](http://gruntjs.com/sample-gruntfile) as well as install and use Grunt plugins. Once you're familiar with that process, you may install this plugin with this command:

```shell
npm install grunt-eol --save-dev
```

Once the plugin has been installed, it may be enabled inside your Gruntfile with this line of JavaScript:

```js
grunt.loadNpmTasks('grunt-eol');
```

## The "eol" task

### Overview
In your project's Gruntfile, add a section named `eol` to the data object passed into `grunt.initConfig()`.

```js
grunt.initConfig({
  eol: {
    options: {
      // Task-specific options go here.
    },
    your_target: {
      // Target-specific file lists and/or options go here.
    },
  },
})
```

### Options

#### options.eol
Type: `String`
Default value: `'lf'`

The line ending you would like to convert to.

#### options.replace
Type: `Boolean`
Default value: `false`

If `true` replace the source file.

### Usage Examples

#### Default Options
In this example, the default options are used to convert the files to `lf` line endings.

```js
grunt.initConfig({
  eol: {
    default_options: {
      files: {
        'tmp/default_options': ['test/fixtures/crlf']
      }
    }
  }
})
```

#### Custom Options
In this example, custom options are used to convert all files to `crlf`.

```js
grunt.initConfig({
  eol: {
    to_crlf_all: {
      options: {
        eol: 'crlf'
      },
      files: [{
        expand: true,
        cwd: 'test/fixtures/',
        src: ['*'],
        dest: 'tmp/to_crlf_all/'
      }]
    }
  }
})
```

In this example, custom options are used to convert all files to `crlf` with inline file replacement.

```js
grunt.initConfig({
  eol: {
    to_crlf_replace: {
      options: {
        eol: 'crlf',
        replace: true
      },
      files: {
        src: [
          './tmp/to_crlf_replace/cr',
          './tmp/to_crlf_replace/crlf',
          './tmp/to_crlf_replace/lf'
        ]
      }
    }
  }
})
```

## Contributing
In lieu of a formal styleguide, take care to maintain the existing coding style. Add unit tests for any new or changed functionality. Lint and test your code using [Grunt](http://gruntjs.com/).

## Release History
_(Nothing yet)_
