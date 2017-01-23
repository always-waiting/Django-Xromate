Genoverse.Track.Positive = Genoverse.Track.extend ( {
  id : 'positiveGeneMap',
  name : 'Positive Samples',
  category : 'Positive GeneMaps',
  info : 'The position in positive sample',
  tags : 'Positive',
  height : 160,
  autoHeight : true,
  hideEmpty : false,
  featureHeight : 6,
  labels : true,
  repeatLabels : true,
  bump : true,
  url : "http://192.168.4.168:9009/cnvs/search?chr=__CHR__&start=__START__&end=__END__",
  parseData: function(data) {
    for (var i in data.results) {
      var cnv = data.results[i];
      cnv.name = cnv.id;
      cnv.label = cnv.abstract ? cnv.abstract : cnv.result;
      if (this.browser.sample && cnv.sample !== this.browser.sample.name && cnv.gainloss === this.browser.cnv.gainloss) {
        delete cnv.position;
        this.insertFeature(cnv);
      }
    }
  },
  setFeatureColor: function(f) {
    f.color = f.gainloss === 'gain' ? '#0000FF' : '#FF0000';
    f.labelColor = f.color;
  },
  populateMenu: function(a, b) {
    var c = {};
    d = [
      ['title', '<a href="http://192.168.4.168:9009/projects/CNV/flowcells/' + a.flowcell + '/samples/' + a.sample + '/cnvs/' + a.chr + ':'+ a.start + '-' + a.end + '">' + a.label + '</a>'],
      ['Sample', '<a href="http://192.168.4.168:9009/projects/CNV/flowcells/' + a.flowcell + '/samples/' + a.sample + '">' + a.sample + '</a>'],
      ['Flowcell', '<a href="http://192.168.4.168:9009/projects/CNV/flowcells/' + a.flowcell + '/samples">' + a.flowcell + '</a>'],
      ['Result', a.result],
      ['Gainloss', a.gainloss],
      ['Location', a.chr + ':' + a.start + '-' + a.end],
      ['Abstract', a.abstract],
      ['description', a.description]
    ];
    for (f in d) d[f][1] && (c[d[f][0]] = d[f][1]);
    return $.extend(c, b);
  }
});
