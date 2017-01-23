Genoverse.Track.DGV = Genoverse.Track.extend({
  id: "dgv",
  name: "DGV",
  category: "DGV variants(hg19)",
  info: "DGV - A curated catalogue of human genomic structural variation",
  tags: ["DGV"],
  url: "/api/annodb/dgv?chr=__CHR__&start=__START__&end=__END__",
  xhrFields: {
    withCredentials: !0
  },
  height: 200,
  autoHeight: true,
  hideEmpty : false,
  featureHeight: 6,
  labels        : true,
  repeatLabels  : true,
  bump          : true,
  parseData: function(d) {
    for (var a in d) {
      f = d[a];
      //console.log(f)
      //console.log(this.browser)
      if (f.end >= this.browser.cnv.end && f.start <= this.browser.cnv.start && (
            this.browser.cnv.gainloss == 'gain' ? f.observedGains > 0 :
            this.browser.cnv.gainloss == 'loss' ? f.observedLosses > 0 : false)) {
        console.log("Good")
        f.name = f.variantAccession;
        f.id = f.name;
        f.label = f.id + ' - ' + f.variantSubtype;
        this.insertFeature(f);
      }
    }
  },
  setFeatureColor: function(a) {
    a.color = a.observedLosses > 0 ? a.observedGains > 0 ? '#DC00DC' : '#FF0000' : a.observedGains > 0 ? '#002FFF' : '#000000';
    a.featureColor = a.color;
  },
  populateMenu    : function(feature) {
    return {
      title   : feature.name,
      Location          : 'chr' + feature.chr + ':' + feature.start + '-' + feature.end,
      "Variant Subtype": feature.variantSubtype,
      "Observed Gains" : feature.observedGains,
      "Observed Losses" : feature.observedLosses,
      "Sample Size"     : feature.sampleSize,
      "Pubmed ID"       : feature.pubmedid,
      "Reference"       : feature.reference,
      "Merged or Sample": feature.mergedOrSample == 'M' ? 'Merged' : 'Sample',
      "Methods"         : feature.method ? $.isArray(feature.method) ? feature.method.join(', ') : feature.method : '-',
      'Genes'           : feature.genes ? $.isArray(feature.genes) ? feature.genes.join(', ') : feature.genes : '-'
    };
  }
});
