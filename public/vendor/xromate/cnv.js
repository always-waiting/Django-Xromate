
;(function ( $, window, document, undefined ) {
  "use strict";
;
  $.fn.cnv = function(parameters) {
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

      returnedValue
    ;
    $allModules.each( function() {
      var
        settings        = ( $.isPlainObject(parameters) )
          ? $.extend(true, {}, $.fn.cnv.settings, parameters)
          : $.extend({}, $.fn.cnv.settings),
        className       = settings.className,
        namespace       = settings.namespace,
        variables       = settings.variables,
        selector        = settings.selector,
        error           = settings.error,

        eventNamespace  = '.' + namespace,
        moduleNamespace = 'module-' + namespace,

        $body           = $('body'),
        body            = $body.data(),
        role            = $body.data('role'),
        $module         = $(this).first(selector.cnv),
        $analyzer       = $module.find(selector.analyzer),
        $process        = $module.find(selector.process),
        $browser        = $module.find(selector.browser),
        $result         = $analyzer.find(selector.result),
        $abstract       = $analyzer.find(selector.abstract),
        $description    = $analyzer.find(selector.description),
        $actions        = $module.find(selector.actions),
        $submit         = $actions.children(selector.submit),
        $confirm        = $actions.children(selector.confirm),
        $reject         = $actions.children(selector.reject),
        $gd             = $module.find(selector.gd),
        $gdbutton       = $gd.children(selector.gdbutton),
        $gdinfo         = $gd.find(selector.gdinfo),


        cnv             = $module.data('cnv'),
        sample          = $module.data('sample'),
        element         = this,
        instance        = $module.data(moduleNamespace),
        elementNamespace,
        id,
        observer,
        module
      ;
      module = {
        initialize: function() {
          module.debug('Initializing cnv', settings);

          module.ensure.actions.all();
          module.bind.events();

          module.apply.cnv();

          if (!module.readyFor.analysis() && !module.readyFor.audition()) {
            // both not ready.
            $module.find(".confirm.button, .reject.button").remove();
            $module.find(".submit.button").remove();
          } else if (module.readyFor.analysis() && module.readyFor.audition()) {
            // both ready.
          } else if (module.readyFor.analysis() || !module.readyFor.audition()) {
            // ready for analysis.
            $module.find(".confirm.button, .reject.button").remove();
          } else if (module.readyFor.audition() || !module.readyFor.analysis()) {
            // ready for audition.
            $module.find(".submit.button").remove();
          }

          module.instantiate();
        },

        readyFor: {
          analysis: function() {
            if ( (body.process == 'unsubmitted' || body.process === 'rejected') && body.username === body.analyst) {
              return true;
            } else {
              return false;
            }
          },
          audition: function() {
            if ((body.process == 'submitted' || body.process === 'confirmed' || body.process === 'rejected') && body.username === body.auditor) {
              return true;
            } else {
              return false;
            }
          }
        },

        apply: {
          cnv: function (data) {
            if (data) { $module.data('cnv', data) }
            cnv = $module.data('cnv');
            module.apply.browser();
            $abstract.hide();
            $description.hide();
            module.apply.analyzer();
          },
          browser: function() {
            module.debug("Apply with genoverse browser", window.genoverse);
            var
              $browser  = $module.find(selector.browser),
              cnv       = $module.data('cnv'),
              browserModule = $browser.data('browserModule'),
              config,
              genoverse
            ;
            $browser.empty();
            config = $.extend({
              container   : $browser,
              width       : $browser.parent().width(),
              genome      : 'grch37',
              chr         : cnv.chr,
              start       : cnv.start,
              end         : cnv.end,
              plugins     : [ 'controlPanel', 'karyotype', 'trackControls', 'resizer', 'focusRegion', 'fullscreen', 'tooltips', 'fileDrop' ],
              tracks      : [
                Genoverse.Track.Scaleline,
                Genoverse.Track.Scalebar,
                //Genoverse.Track.Cytoband,
                Genoverse.Track.CNV,
                Genoverse.Track.Positive,
                Genoverse.Track.Pubmed,
                Genoverse.Track.Syndrome,
                Genoverse.Track.OMIM,
                Genoverse.Track.OmimSyndrome,
                Genoverse.Track.DGV,
                Genoverse.Track.RefGene,
                Genoverse.Track.DecipherCNV,
                Genoverse.Track.ClinVar,
                Genoverse.Track.GeneReviews
              ]
            }, $body.data(), $module.data());
            module.debug('Apply CNV in browser', $browser);
            genoverse = new Genoverse(config);
            $module.data('browserModule', genoverse);
            return genoverse;
          },


          analyzer: function() {
            $process.html(variables.text[cnv.process]);
            $analyzer.form('set values', cnv);
          }
        },

        ensure: {
          actions: {
            all: function() {
              module.ensure.actions.submit();
              module.ensure.actions.confirm();
              module.ensure.actions.reject();
            },
            submit: function() {
              if (!sample) {
                return;
              }
              if ($submit.length == 0 && (sample.analyst === body.username)) {
                $submit = $('<div class="disabled ui blue submit button">提交分析</div>')
                  .data('content', settings.popup['submit'])
                  .popup()
                  .appendTo($actions);
              }
              module.debug('process', cnv.process);
              if (cnv.process == 'unsubmitted' || cnv.process == 'rejected' || $analyzer.form('get value', 'result') !== cnv.result) {
                $submit.removeClass('disabled');
              } else {
                $submit.addClass('disabled');
              }
              return $submit;
            },
            confirm: function() {
              if (!sample) {
                return;
              }
              if ($confirm.length == 0 && (sample.auditor === body.username)) {
                $confirm = $('<div class="disabled ui positive confirm button">确认结论</div>')
                  .data('content', settings.popup['confirm'])
                  .popup()
                  .appendTo($actions);
              }
              if (cnv.process == 'submitted' && $analyzer.form('get value', 'result') === cnv.result) {
                $confirm.removeClass('disabled');
              } else {
                $confirm.addClass('disabled');
              }
              return $confirm;
            },
            reject:   function() {
              if (!sample) {
                return;
              }
              if ($reject.length == 0 && sample.auditor === body.username) {
                $reject = $('<div class="disabled ui negative reject button">驳回结论</div>')
                  .data('content', settings.popup['confirm'])
                  .popup()
                  .appendTo($actions);
              }
              if ((cnv.process === 'submitted' || cnv.process == 'confirmed') && $analyzer.form('get value', 'result') === cnv.result) {
                $reject.removeClass('disabled');
              } else {
                $reject.addClass('disabled');
              }
              return $reject;
            }
          }
        },


        activate: {
          reset: function() {
            module.error('Unimplemented');
          },
          submit: function() {
            module.activate.none();
            $submit.removeClass('disabled');
          },
          confirm: function() {
            module.activate.none();
            $confirm.removeClass('disabled');
            $reject.removeClass('disabled');
          },
          reject: function() {
            module.activate.none();
            $reject.removeClass('disabled');
          },
          none: function() {
            $submit.addClass('disabled');
            $confirm.addClass('disabled');
            $reject.addClass('disabled');
          },
          default: function() {
            module.ensure.actions.all();
          }
        },

        instantiate: function() {
          module.verbose('Storing instance of modal');
          instance = module;
          $module
            .data(moduleNamespace, instance)
            ;
        },

        bind: {
          events: function() {
            module.debug("Bind events for result changing", $result);
            $result.find('.dropdown').dropdown({
              onChange: module.event.result.change
            });
            $submit.click(module.event.action.submit);
            $confirm.click(module.event.action.confirm);
            $reject.click(module.event.action.reject);
            $gdbutton.click(module.event.action.gd.search);
            $description.find('textarea').on('valuechange', module.event.description.change);
            $abstract.find('input').on('valuechange', module.event.abstract.change);
          }
        },
        event: {
          abstract    : {
            change: function() {
              if (typeof cnv.abstract !== 'undefined' && $(this).val() !== cnv.abstract) {
                module.activate.submit();
              } else {
                module.activate.default();
              }
            }
          },
          description : {
            change: function(event, previous) {
              if (typeof cnv.description !== 'undefined' && $(this).val() !== cnv.description) {
                module.activate.submit();
              } else {
                module.activate.default();
              }
            }
          },
          result: {
            change: function(value, text, $choice) {
              module.debug("Result changing", value, $choice);
              $module.find('.horizontal.teal.label').remove();
              $analyzer.form({ onSucesss: function() {} });
              var
                result  = cnv.result,
                description = module.get.description(value),
                submitLabel = '<div class="ui tiny teal horizontal label">Submitted</div>',
                labelSelector
              ;
              module.debug('Submitted result is ', result);
              if (result) {
                labelSelector = (result == value ? '.dropdown .text, ' : '') + '.item[data-value=' + result + ']';
                $result.find(labelSelector).prepend(submitLabel);
                if (result == value) {
                  module.activate.default();
                  $analyzer.form('set values', cnv);
                } else if (result != value) {
                  module.activate.submit();
                  $analyzer.form('set values', {
                    description : module.get.description(value),
                    abstract    : module.get.abstract(value)
                  });
                } else {
                  module.activate.none();
                }
              } else {
                module.debug('Changing with no result');
                module.activate.submit();
                $analyzer.form('set values', {
                  description : module.get.description(value),
                  abstract    : module.get.abstract(value)
                });
              }
              switch (value) {
                case 'normal':
                  $abstract.hide();
                  break;
                case 'polymorphism':
                  $abstract.hide();
                  $description.hide();
                  break;
                case 'other':
                  $abstract.hide();
                  $description.show();
                  break;
                case 'unknown':
                  $abstract.show();
                  $description.show();
                  break;
                case 'exception':
                  $abstract.show();
                  $description.show();
                case 'mosaic':
                  $abstract.show();
                  $description.show();
                  break;
              }
              settings.onChange(value, text);
            },
            reset: function() {
            },
            clear: function() {
            }
          },

          action: {
            gd : {
              search: function() {
                module.debug("Get GD data");
                cnv = $module.data("cnv");
                module.debug(cnv);
                $gdbutton.api({
                  url: module.get.url.gdsearch(cnv),
                  method: "GET",
                  on: "now",
                  onSuccess: module.event.gd.success,
                  onError: module.event.gd.error,
                  onFailure: module.event.gd.failure,
                });
              },
            },
            submit: function() {
              var
                fields = $module.find('.field:visible [name]').map(function () { return $(this).attr('name'); }),
                values = $module.form('get values', fields.toArray()),
                $content = $('<div class="description"></div>')
                  .append(module.create.list(values))
              ;
              $analyzer.form({
                fields: module.get.validator(fields),
              //  on        : 'analyze',
                onSuccess : function() {
                  var mod = module.create.modal({
                    header : '提交分析结论',
                    content : $content
                  });

                  $('.modal.form').modal({
                    onApprove : function(){
                      module.debug('Approved');
                      module.action.patch( $.extend(values, {process: 'submitted'}) );
                    }
                  }).modal("show");
                }
              }).form('validate form');
            },
            confirm: function() {
              var
                fields = $module.find('.field:visible [name]').map(function () { return $(this).attr('name'); }),
                values = $module.form('get values', fields.toArray()),
                $content = $('<div class="description"></div>')
                  .append(module.create.list(values))
              ;

              $analyzer.form({
                fields : module.get.validator(fields),
               // on        : 'analyze',
                onSuccess: function() {
                  module.create.modal({
                    header : '审核分析结论',
                    content : $content,
                  }).modal({
                    onApprove : function(){
                      module.debug('Approved');
                      module.action.patch(
                        {process : 'confirmed'}
                      );
                    }
                  }).modal('show');
                }
              }).form('validate form');
            },
            reject: function() {
              var
                fields = $module.find('.field:visible [name]').map(function () { return $(this).attr('name'); }),
                values = $module.form('get values', fields.toArray()),
                $content = $('<div class="description"></div>')
                  .append(module.create.list(values))
                  .append('<div class="field"><label>请填写驳回原因:</label><div class="ui fluid icon input"><input type="text" name="rejection"></div></div>')
              ;

              $analyzer.form({
                fields : module.get.validator(fields),
                //on        : 'analyze',
                onSuccess: function() {
                  module.create.modal({
                    header : '驳回分析结论',
                    content : $content,
                  }).modal({
                    onApprove : function(){
                      module.debug('Approved');
                      var $modal = $(this);
                      $modal.form({
                        fields: {
                          rejection: {
                            identifier: 'rejection',
                            rules: [
                              { type: 'empty', prompt: 'Please enter reject reason.' }
                            ]
                          }
                        },
                        inline: true,
                        onSuccess: function(){
                          module.action.patch({
                            process: 'rejected',
                            rejection: $modal.form('get value', 'rejection')
                          });
                        }
                      });
                      var validation = $modal.form('validate form');
                      console.log(validation);
                      if(! validation){return false;}
                    }
                  }).modal('show');
                }
              }).form('validate form');
            }
          },

          process: {
            unsubmitted: function () {
              $module.children(selector.label).html('未提交').removeClass('orange').removeClass('teal').addClass('red');
              $module.find(selector.confirm).addClass('disabled');
            },
            submitted: function () {
              $module.children(selector.label).html('已提交/未审核').removeClass('red').removeClass('teal').addClass('orange');
              if ($body.data('role') === 'auditor') {
                $module.find(selector.confirm).removeClass('disabled');
              }
            },
            confirmed: function () {
              $module.children(selector.label).html('已审核').removeClass('red').removeClass('orange').addClass('teal');
              if ($body.data('role') === 'auditor') {
                $module.find(selector.confirm).removeClass('disabled');
              }
            }
          },

          cnv: {
            success: function(data) {
              module.debug("Successed", data, this);
              module.apply.cnv(data);
              return true;
            },
            failure: function(data) {
              module.debug('Failure', data);
            },
            error: function(data) {
              module.debug("Error: ",data, this);
            }
          },

          gd: {
            success: function(data) {
              module.debug("Successed", data, this);
              // 构建GD结果报告表
              var result = data.result;
              module.debug($gdinfo);
              //先确定没有，有删除
              $gdinfo.empty();
              //在这里生成报表
              $gdinfo.append('<table class="ui celled padded structured table"><thead></thead><tbody></tbody></table>');
              $.each(result, module.event.gd.insertoneresult);// 目前只有1个，展现形式有所差异
              return true;
            },
            error: function(data) {
              module.debug("Error: ", data, this);  
            },
            failure: function(data) {
              module.debug("Failure: ", data, this);
            },
            insertoneresult: function(k,v) {
              var 
                $tbody = $gdinfo.find("tbody"),
                cnvrows = v.cnv_paper.length,
                patientrows = v.patient.length,
                ncbi = "https://www.ncbi.nlm.nih.gov/pubmed/?term=",
                message = v.resultMessage.replace(/null\n?/g,"").replace(/\n/g,"<br>");
              module.debug(cnvrows);
              $('<tr><td>Position</td><td>'+k+'</td></tr>').appendTo($tbody);
              if (message) {
                $('<tr><td>ResultMessage</td><td><p>'+
                  message+'</p></td></tr>'
                ).appendTo($tbody);
              }
              $('<tr><td>SampleResult</td><td>'+v.sampleResult+'</td></tr>').appendTo($tbody);
              $.each(v.cnv_paper, function(i, val) {
                var href = ncbi+val.pmid;
                if (i == 0) {
                  $('<tr><td rowspan='+cnvrows+'>CNVPapers</td><td><a target="_blank" href="'+href+'">'+val.pmid+'</a></td></tr>').appendTo($tbody);
                } else {
                  $('<tr><td><a target="_blank" href="'+href+'">'+val.pmid+'</a></td></tr>').appendTo($tbody);
                }
              });
              $.each(v.patient, function(i, val) {
                var href = ncbi+val.pmid;
                if (i == 0 ){
                  if (val.pmid) {
                    $('<tr><td rowspan='+patientrows+
                      '>Patients</td><td>'+val.relatedGenes+
                      '&nbsp&nbspPMID[<a target="_blank" href="'+
                      href+'">'+val.pmid+'</a>]</td></tr>'
                    ).appendTo($tbody);
                  } else {
                    $('<tr><td rowspan='+
                      patientrows+'>Patients</td><td><p>'+
                      val.reference.replace(/(\[\d+\])/g,'<br>$1').replace(/^<br>/,"")+
                      '</p></td></tr>'
                    ).appendTo($tbody);
                  }
                } else {
                  if (val.pmid) {
                    $('<tr><td>'+val.relatedGenes+
                      '&nbsp&nbspPMID[<a target="_blank" href="'+
                      href+'">'+val.pmid+
                      '</a>]</td></tr>'
                    ).appendTo($tbody);
                  } else {
                    $('<tr><td><p>'+
                      val.reference.replace(/(\[\d+\])/g,'<br>$1').replace(/^<br>/,"")+
                      '</p></td></tr>'
                    ).appendTo($tbody);
                  }
                }
              });
            },
          },

        },

        create: {
          modal: function(modal) {
            module.debug('Create modal', modal);
            $('.modal').remove();
            var $modal = $('<div class="ui modal form"></div>');
            //$modal.addClass(modal.class);
            $('<i class="close icon"></i>').appendTo($modal);
            $('<div class="header"></div>').html(modal.header).appendTo($modal);
            $('<div class="content"></div>').html(modal.content).appendTo($modal);
            modal.actions = $('<div class="ui buttons"></div>');
            $(['negative', 'positive']).each(function() {
              modal.actions.append('<div class="ui ' + this + ' button">' + variables.text[this] + '</div>');
            });
            $('<div class="actions"></div>').html(modal.actions).appendTo($modal);
            $modal.appendTo($module);
            return $modal;
          },
          list: function(list) {
            module.debug('Create list table', list);
            var $table = $('<table class="ui definition table"></div>');
            for (var key in list) {
              $('<tr></tr>').append($('<td></td>').html(key)).append($('<td></td>').html(variables.text[list[key]] || list[key])).appendTo($table);
            }
            return $table;
          }
        },

        action: {
          patch: function(data) {
            module.debug('PATCHING');
            $module.api({
              on: 'now',
              action: 'cnv',
              urlData: $body.data(),
              data: data,
              method: 'PATCH',
              onError: module.event.cnv.error,
              onFailure: module.event.cnv.failure,
              onSuccess: module.event.cnv.success
            });
          },
        },

        get: {
          url: {
            projects: function() {
              return "/projects";
            },
            project: function() {
              return module.get.url.projects() + "/" + $('body').data('project');
            },
            flowcells: function() {
              return module.get.url.project() + "/flowcells";
            },
            flowcell: function() {
              return module.get.url.flowcells() + "/" + $('body').data('flowcell');
            },
            samples: function() {
              return module.get.url.flowcell() + "/samples";
            },
            sample : function () {
              return module.get.url.samples() + "/" + $('body').data('sample');
            },
            chromosome: function () {
              return module.get.url.sample() + "/chromosomes/" + $('body').data('chromosome');
            },
            cnvs: function() {
              return module.get.url.sample() + "/cnvs";
            },
            merge: function() {
              return module.get.url.cnvs() + "/merge";
            },
            cnv: function (cnv) {
              return module.get.url.cnvs() + "/" + (cnv.location ? cnv.location : "chr" + cnv.chr + ":" + cnv.start + "-" + cnv.end);
            },
            gdsearch: function(cnv) {
              var path = cnv.position ? cnv.position : "chr" + cnv.chr + ":" + cnv.start + "-" + cnv.end;
              path = path + ":" + cnv.gainloss;
              return "/gd/search/" + path;
            },
          },
          chromosome: {
            name: function() {
              return '' + $module.data('chromosome');
            },
            start: function() {
            },
            end: function() {
            }
          },
          abstract    : function(result) {
            var abstract;
            switch(result) {
              case 'unknown':
                abstract = '未知';
                break;
              default:
                abstract = '';
                break;
            }
            return abstract;
          },
          description: function(result) {
            var description;
            switch(result) {
              case 'normal':
                description = '未见明显异常';
                break;
              case 'unknown':
                description = '';
                break;
              case 'polymorphism':
                description = '{chr}号染色体{gainloss}区域，为多态性。';
                break;
              default:
                description = '';
            }
            return description.format({chr: cnv.chr, gainloss: variables.text[cnv.gainloss]});
          },
          validator: function(fields) {
            module.debug('get validator', $(fields));
            var result =  $module.form('get value', 'result');
            var out = $(fields).map(function() {
              module.debug("field", this);
              if (this == 'abstract' && result == 'mosaic' ) {
              } else if (this == 'description' && result === 'unknown') {
              } else {
                return settings.validator[this];
              }
            });
            module.debug('outout',out);
            return out;
          },
          fields: function(fields) {
            module.debug('get fields', $(fields));
            return $(fields).map(function() {
              module.debug('field', this);
              return $module.find(settings.selector[this]).first();
            });
          }
        },
        debug: function() {
          if(settings.debug) {
            if(settings.performance) {
              module.performance.log(arguments);
            }
            else {
              module.debug = Function.prototype.bind.call(console.info, console, settings.name + ':');
              module.debug.apply(console, arguments);
            }
          }
        },
        verbose: function() {
          if(settings.verbose && settings.debug) {
            if(settings.performance) {
              module.performance.log(arguments);
            }
            else {
              module.verbose = Function.prototype.bind.call(console.info, console, settings.name + ':');
              module.verbose.apply(console, arguments);
            }
          }
        },
        error: function() {
          module.error = Function.prototype.bind.call(console.error, console, settings.name + ':');
          module.error.apply(console, arguments);
        },
        performance: {
          log: function(message) {
            var
              currentTime,
            executionTime,
            previousTime
              ;
            if(settings.performance) {
              currentTime   = new Date().getTime();
              previousTime  = time || currentTime;
              executionTime = currentTime - previousTime;
              time          = currentTime;
              performance.push({
                'Name'           : message[0],
                'Arguments'      : [].slice.call(message, 1) || '',
                'Element'        : element,
                'Execution Time' : executionTime
              });
            }
            clearTimeout(module.performance.timer);
            module.performance.timer = setTimeout(module.performance.display, 100);
          },
        },
        invoke: function(query, passedArguments, context) {
          var
            object = instance,
          maxDepth,
          found,
          response
            ;
          passedArguments = passedArguments || queryArguments;
          context         = element         || context;
          if(typeof query == 'string' && object !== undefined) {
            query    = query.split(/[\. ]/);
            maxDepth = query.length - 1;
            $.each(query, function(depth, value) {
              var camelCaseValue = (depth != maxDepth)
              ? value + query[depth + 1].charAt(0).toUpperCase() + query[depth + 1].slice(1)
              : query
              ;
            if( $.isPlainObject( object[camelCaseValue] ) && (depth != maxDepth) ) {
              object = object[camelCaseValue];
            }
            else if( object[camelCaseValue] !== undefined ) {
              found = object[camelCaseValue];
              return false;
            }
            else if( $.isPlainObject( object[value] ) && (depth != maxDepth) ) {
              object = object[value];
            }
            else if( object[value] !== undefined ) {
              found = object[value];
              return false;
            }
            else {
              return false;
            }
            });
          }
          if ( $.isFunction( found ) ) {
            response = found.apply(context, passedArguments);
          }
          else if(found !== undefined) {
            response = found;
          }
          if($.isArray(returnedValue)) {
            returnedValue.push(response);
          }
          else if(returnedValue !== undefined) {
            returnedValue = [returnedValue, response];
          }
          else if(response !== undefined) {
            returnedValue = response;
          }
          return found;
        }
      };
      if(methodInvoked) {
        if(instance === undefined) {
          module.initialize();
        }
        module.invoke(query);
      }
      else {
        if(instance !== undefined) {
          instance.invoke('destroy');
        }
        module.initialize();
      }
    });
    return (returnedValue !== undefined)
      ? returnedValue
      : this
    ;
  };

  $.fn.cnv.settings = {
    name          : 'cnv',
    namespace     : 'cnv',

    debug         : false,
    verbose       : false,
    performance   : false,

    onChange      : function () { },
    onInited      : function () { },
    onError       : function () { },
    oncnv      : function () { },

    error         : {
      method      : 'The method you called is not defined'
    },

    editable      : true,

    validator    : {
      result: {
        identifier: 'result',
        rules: [{
          type: 'empty'
        }]
      },
      abstract: {
        identifier: 'abstract',
        rules: [{
          type: 'empty',
          prompt: 'Please write label for the result'
        }]
      },
      description: {
        identifier: 'description',
        rules: [{
          type: 'empty',
          prompt: 'Please write description for the result'
        }]
      },
    },

    selector      : {
      cnv         : '.cnv.container, .cnv.grid',
      browser     : '.browser',
      analyzer    : '.analyzer',
      title       : '.title',
      process     : '.process.label',
      result      : '.field:has([name=result])',
      abstract    : '.field:has([name=abstract])',
      description : '.field:has([name=description])',
      actions     : '.buttons',
      gd          : '.gd',
      gdbutton    : '.button',
      gdinfo      : '.container .info',
      error       : '.error',
      reset       : '.reset',
      submit      : '.submit',
      confirm     : '.confirm',
      reject      : '.reject',
    },

    popup         : {
      submit      : '请提交该条记录，留待审核人员确认',
      confirm     : '确认即接受本条记录的分析结论',
      reject      : '该条记录的分析结论错误或其他原因需要修改'
    },

    variables     : {
      text        : {
        unsubmitted   :   '未分析',
        submitted     :   '已提交',
        confirmed     :   '已确认',
        rejected      :   '已驳回',
        negative      :   '取消',
        positive      :   '确定',

        gain          : '重复',
        loss          : '缺失',
        unknown       : '未知',
        normal        : '正常',
        polymorphism  : '多态',
        exception     : '异常',
        mosaic        : '嵌合'
      },
      header      : {
        submit    : '提交分析结论',
        confirm   : '确认分析结论',
        reject    : '驳回分析结论'
      }
    }
  };

})( jQuery, window , document );

