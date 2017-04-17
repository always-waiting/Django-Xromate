// namespace
window.semantic = {
  handler: {}  
};

// Allow for console.log to not break IE
if (typeof window.console == "undefined" || typeof window.console.log == "undefined") {
  window.console = {
    log  : function() {},
    info : function(){},
    warn : function(){}
  };
}
if(typeof window.console.group == 'undefined' || typeof window.console.groupEnd == 'undefined' || typeof window.console.groupCollapsed == 'undefined') {
  window.console.group = function(){};
  window.console.groupEnd = function(){};
  window.console.groupCollapsed = function(){};
}
if(typeof window.console.markTimeline == 'undefined') {
  window.console.markTimeline = function(){};
}
window.console.clear = function(){};

//ready event
semantic.ready = function() {
  $('[data-url]').each( function (n, v) {
    v = $(v);
    v.visibility({
      onTopVisible: function(calculations) {
        //console.log(calculations)
        v.api({
          on: 'now',
          url: v.data().url,
          onSuccess: function (data){
            console.log(data)
            $(this).html(data);
            if (v.hasClass('label')) {
              if (data) {
                v.addClass('teal');
              }
            }
          }
        });
      }
    });
  });
}

$(document).ready(function() {
  $('.top.menu').xromatenav() 
  $('.samples').samples()
  $('.ui.dropdown').dropdown()
  semantic.ready()
})

