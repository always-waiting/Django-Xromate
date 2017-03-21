Genoverse.Track.GeneReview = Genoverse.Track.extend({
  id: "GeneReviews",
  name: "GeneReviews",
  category: "GeneReviews(hg19)",
  info: "GeneReviews - an international point-of-care resource for busy clinicians",
  tags: ["GeneReviews"],
  url: "/api/annodb/genereview?chr=__CHR__&start=__START__&end=__END__",
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
    console.log('genereview gene as below:');
    for (var a in d) {
      f = d[a];
      if (f.start < this.browser.cnv.end && f.end > this.browser.cnv.start) {
        f.label = f.gene_symbol;
        console.log(f);
        this.insertFeature(f);
      }
    }
  },
  setFeatureColor: function(a) {
    a.color = '#FF0000';
    a.labelColor = a.color;
  },
  populateMenu : function(feature) {
    var accessions = feature.accession.split(";");
    accessions.pop();
    var accessions_content = '';
    for (var i in accessions) {
      var genereview_url = "/vendor/genereview/" + accessions[i] + '.html';
      accessions_content += '<a href="' + genereview_url + '">' + accessions[i] + '</a>;';
    }
    var menu = {
      title       : feature.gene_symbol,
      gene_symbol : feature.gene_symbol,
      chr         : feature.chr,
      start       : feature.start,
      end         : feature.end,
      accession   : accessions_content,
      description : feature.description,
    }
    return menu;
  }
});
