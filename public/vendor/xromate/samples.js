// 处理/xromate/projects/<projcet>/flowcells/<flowcell>/路由
// 产生的前端动作
;(function ( $, window, document, undefined ) {
  "use strict";

  $.fn.samples = function(parameters) {
    var 
      $allModules     = $(this),
      time            = new Date().getTime(),
      performance     = [],
      query           = arguments[0],
      methodInvoked   = (typeof query == 'string'),
      queryArguments  = [].slice.call(arguments, 1),
      requestAnimationFrame = window.requestAnimationFrame
        || window.mozRequestAnimationFrame
        || window.webkitRequestAnimationFrame
        || window.msRequestAnimationFrame
        || function(callback) { setTimeout(callback, 0); },
      returnedValue;
    $allModules.each(function(){
      var
        settings        = ( $.isPlainObject(parameters) )
          ? $.extend(true, {}, $.fn.samples.settings, parameters)
          : $.extend({}, $.fn.samples.settings),
        className       = settings.className,// 无用?
        namespace       = settings.namespace,
        variables       = settings.variables,
        selector        = settings.selector,
        error           = settings.error,
        eventNamespace  = '.' + namespace,
        moduleNamespace = 'module-' + namespace,
        $body           = $('body'),
        body            = $body.data(),
        $module         = $(this).first(selector.samples),
        $samples        = $module.find(selector.sample),
        $analyst        = $samples.find(selector.analyst),
        $auditor        = $samples.find(selector.auditor),
        users,
        usersChooser,
        usersChooserDisabled = true,
        element         = this,
        instance        = $module.data(moduleNamespace),
        elementNamespace,
        id,
        observer,
        module
      ;
      module = {
        initialize: function() {
          module.debug('Initializing samples', settings);
          $.api({
            url: '/xromate/profile?fields=role',
            on: 'now',
            onSuccess: function (profile) {
              //console.log(profile)
              if (profile.role === 'master' || profile.role === 'owner') {
                usersChooserDisabled = false;
                // Get users list.
                $.api({
                  url: '/xromate/users',
                  on : 'now',
                  onSuccess: function(response) {
                     module.verbose('Got users', response);
                     settings.variables.users = response;
                     module.bind.events();
                  }
                })
              }
            }
          });
          //module.instantiate();
        }, // initialize done
        bind: {
          events: function() {
            module.verbose('Binding events', $analyst);
            $samples.each(function (index, sample) {
              var 
                $sample = $(sample),
                $analyst = $sample.find(selector.analyst),
                $auditor = $sample.find(selector.auditor)
              ;
              //console.log($analyst.text() + " -> " + $auditor.text())
              $analyst.each(function() {
                var defaultText = $(this).text();
                var $chooser = module.create.users.chooser('analyst');
                $chooser.dropdown({
                  apiSettings: {
                    url: '/users/search?q={query}'
                  },
                  onChange: function (value, text, $choice) {
                    if (value && text != defaultText) {
                      $sample.api({
                        url: location.pathname + '/samples/' + $sample.data('name'),
                        method: 'PATCH',
                        data: {
                          analyst: value
                        },
                        on: 'now'
                      })
                    }
                  }
                });
              })
            })
          },// bind.events done
        }, // bind done
        debug: function() {
          if(settings.debug) {
            if(settings.performance) {
              module.performance.log(arguments);
            } else {
              module.debug = Function.prototype.bind.call(console.info, console, settings.name + ':');
              module.debug.apply(console, arguments);
            }
          }
        },
        verbose: function() {
          if(settings.verbose && settings.debug) {
            if(settings.performance) { 
              module.performance.log(arguments);
            } else {
              module.verbose = Function.prototype.bind.call(console.info, console, settings.name + ':');
              module.verbose.apply(console, arguments);
            }
          }
        },
      ///////////////////
      };

      if (methodInvoked) {
        module.initialize()
      } else {
        module.initialize()
      }
    });
    return (returnedValue !== undefined)
    ? returnedValue
    : this
  };

  $.fn.samples.settings = {
    name          : 'samples',
    namespace     : 'samples',
    debug         : true,
    verbose       : true,
    performance   : false,
    
    onChange      : function () { },
    onInited      : function () { },
    onError       : function () { },
    error         : {
      method      : 'The method you called is not defined'
    },

    editable      : true,

    variables     : {
    },

    selector      : {
      samples     : '.samples',
      sample      : '.sample',
      analyst     : '.analyst',
      auditor     : '.auditor',
      error       : '.error',
    },
    

  };
})( jQuery, window , document );
