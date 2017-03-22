Genoverse.Track.ClinVar = Genoverse.Track.extend({
  id: "clinvar",
  name: "ClinVar",
  category: "ClinVar(hg19)",
  info: "ClinVar - aggregates information about genomic variation and its relationship to human health",
  tags: ["ClinVar"],
  url: "/api/annodb/clinvar/__CHR__:__START__-__END__",
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
      var start = f.start > this.browser.cnv.start ? f.start : this.browser.cnv.start;
      var end = f.end < this.browser.cnv.end ? f.end : this.browser.cnv.end;
      var percent = (end - start + 1) / (f.end - f.start + 1);
      //console.log(percent)
      if ( f.assembly == 'GRCh37' && (
          (this.browser.cnv.gainloss == 'gain' && (f.type == 'copy number gain' || f.type == 'Duplication')) ||
          (this.browser.cnv.gainloss == 'loss' && (f.type == 'copy number loss' || f.type == 'Deletion'))) &&
          percent >= 0.5
      ) {
        f.label = f.name;
        f.percent = percent;
        console.log(f);
        this.insertFeature(f);
      }
    }
  },
  setFeatureColor: function(a) {
    if (a.type == 'copy number gain' || a.type == 'Duplication') {
      a.color = a.percent == 1 ? '#00008B' : '#1E90EF';
    } else if (a.type == 'copy number loss' || a.type == 'Deletion') {
      a.color = a.percent == 1 ? '#FF0000' : "#FF7256";
    }
    a.labelColor = a.color;
  },
  populateMenu : function(feature) {
    var accession_url = 'http://www.ncbi.nlm.nih.gov/clinvar/' + feature.rcv_accession;
    var pubmed_url = "http://www.ncbi.nlm.nih.gov/pubmed/" + feature.pubmeds;
    var genereview_url = "http://www.ncbi.nlm.nih.gov/books/" + feature.gene_reviews;
    var menu = {
      title       : feature.name,
      accession   : '<a href="' + accession_url + '">' + feature.rcv_accession + "</a>",
      chr         : feature.chr,
      start       : feature.start,
      end         : feature.end,
      type        : feature.type,
      clinsign    : feature.clinsign,
      source      : feature.origin,
      percent     : feature.percent.toFixed(2) * 100 + '%',
      pubmeds     : '<a href="' + pubmed_url + '">' + feature.pubmeds + "</a>",
      assembly    : feature.assembly,
      genereviews : '<a href="' + genereview_url + '">' + feature.gene_reviews + "</a>"
    }
    return menu;
  }
});
