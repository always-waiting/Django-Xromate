Genoverse.Track.CNV = Genoverse.Track.extend({
  id      : 'cnv',
  name    : 'CNV',
  category: 'CNV',
  info    : "CNV - Copy Number Variants of Samples",
  height  : 50,
  autoHeight  : true,
  hideEmpty   : false,
  featureHeight: 6,
  tags: [],
  labels: true,
  repeatLabels: true,
  bump: true,
  url: false,
  highlighted: false,

  getData: function () {
    var result2cn = {
      normal: '正常', polymorphism: '多态', unknown: '未知', exception: '异常', mosaic: '嵌合', monosome: '单体', trisome: '三体', tetrasome: '四体', loss : '缺失', gain : '重复',
    };
    f = $.extend({}, this.browser.cnv);
    f.position = undefined;
    f.location = "chr" + f.chr + ":" + f.start + '-' + f.end;
    if ('undefined' === typeof f.gainloss || !f.gainloss) {
      f.gainloss = f.type === "Mosaic" ? "mosaic" : (f.copy < (((this.browser.gender === "male" && this.browser.chr === "X") || this.browser.chr === 'Y' ) ? 1 : 2 ) ? "loss" : "gain");
    }
    if (!f.name) {
      f.name = f.location;
    }
    f.label = result2cn[f.gainloss];
    this.insertFeature(f);
    return $.Deferred().resolveWith(this);
  },
  populateMenu: function (feature) {
    var c = {},
      d = [
      [ 'title', feature.name ],
      [ 'Flowcell', this.browser.flowcell ],
      [ 'Sample', this.browser.sample ? this.browser.sample.name : undefined],
      [ 'Location',feature.location],
      [ "Copy", feature.copy ],
      [ 'Log2', feature.log2 ],
      [ 'Result', feature.result ],
      [ 'Description', feature.description ],
    ];
    for (f in d) "undefined" !== typeof d[f][1] && (c[d[f][0]] = d[f][1]);
    return c;
  },
  setFeatureColor: function (f) {
    f.featureColor = f.color = f.gainloss == "mosaic" ? "#00FF00" : (f.gainloss == "loss" ? "#FF0000" : "#0000FF");
    if (!this.highlighted) {
      this.browser.addHighlight({start: f.start, end: f.end, label: [ f.label ], color: f.color});
      this.highlighted = true;
    }
  },
});
