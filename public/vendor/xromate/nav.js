;(function ($, window, document, undefined) {
  'use strict';
  $.fn.xromatenav = function(parameters) {
    var 
      $allModules = $(this),
      time = new Date().getTime(),
      performance = [],
      query = arguments[0],
      methodInvoked = (typeof query=='string'),
      queryArguments = [].slice.call(arguments, 1),
      requestAnimationFrame = window.requestAnimationFrame
        || window.mozRequestAnimationFrame
        || window.webkitRequestAnimationFrame
        || window.msRequestAnimationFrame
        || function(callback) { setTimeout(callback, 0); },
      returnedValue
    
    //console.log(this)
    //console.log($allModules);
    $allModules.each( function() {
      var
        settings        = ( $.isPlainObject(parameters) )
          ? $.extend(true, {}, $.fn.xromatenav.settings, parameters)
          : $.extend({}, $.fn.xromatenav.settings),
        className       = settings.className,
        namespace       = settings.namespace,
        variables       = settings.variables,
        selector        = settings.selector,
        error           = settings.error,

        eventNamespace  = '.' + namespace,
        moduleNamespace = 'module-' + namespace,

        $body           = $('body'),
        body            = $body.data(),
        // 这里定义需要的变量
        $nav            = $(selector.nav),
        app             = $(selector.appname).first(),
        appname         = app.text(),
        $headerfield    = $(selector.headerfield),
        $rightmenu      = $nav.find(selector.rightmenu),
        module
      ;
      module = {
        initialize: function() {
          module.debug('Initializing xromate', settings);
          module.ensure.actions.all();
        },
        ensure: {
          actions: {
            all: function() {
              module.ensure.actions.menuset()
            },
            menuset: function() {
              if (appname == 'Xromate') {
                //alert("改变抬头适应xromate网站")
                //初始化
                $rightmenu.children('div').each(function() {
                  if (this.id == 'app_list' || this.id == 'logout') {
                    module.debug("什么也不做,保留这些选项")
                  } else if (this.id == 'userpage'){
                    module.debug("设置用户页面链接,不同网站不同链接")
                  } else {
                    module.debug("删除" + $(this).html())
                    $(this).remove()
                  }
                })
                $rightmenu.prepend(
                  "<div class='ui dropdown item'><a>Statistics</a><i class='dropdown icon'></i><div class='menu'><a class='item'>Samples</a><a class='item'>CNVs</a><a class='item'>CNVs Search</a></div></div>"
                )
                $rightmenu.prepend(
                  "<div class='ui dropdown item'><a>Projects</a><i class='dropdown icon'></i><div class='menu'><a class='item' href='/xromate/projects/CNV/'>CNV</a><a class='item' href='/xromate/projects/PGS/'>PGS</a><a class='item' href='/xromate/projects/MCC/'>MCC</a></div></div>"
                )
                $rightmenu.prepend(
                  "<div class='ui search item focus'><div class='ui inverted transparent left icon input'><i class='search icon'></i><input type='text' placeholder='Search...' class='prompt' autocomplete='off'></div><div class='results'></div></div>"
                )
              }
            },
          }
        },
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
    ;
  };

  $.fn.xromatenav.settings = {
    name            : 'xromatenav',
    namespace       : 'xromatenav',
    
    debug           : true,
    verbose         : false,
    performance     : false,
    
    onChange        : function() {},
    onInited        : function() {},
    onError         : function() {},
    
    error           : {
      method        : 'The method you called is not defined'  
    },

    editable        : true,
    
    selector        : {
      nav           : '.top.fixed.inverted.menu',
      appname       : '#app_list a',
      headerfield   : '#app_header',
      rightmenu     : '.right.menu',
    },

    variables       : {  
    }
  }
})(jQuery, window, document)
