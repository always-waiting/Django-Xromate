Genoverse.Track.DecipherCNV = Genoverse.Track.extend({
  id: "decipherCNV",
  name: "DECIPHER: CNVs",
  category: "DECIPHER CNVs",
  info: "Copy-number variants observed in other DECIPHER patients",
  tags: ["Patients", "DECIPHER", "Other"],
  url: "/api/annodb/deciphercnv?chr=__CHR__&start=__START__&end=__END__",
  height: 200,
  featureHeight: 6,
  autoheight: true,
  hideEmpty : false,
  labels        : true,
  repeatLabels  : true,
  bump          : true,
  parseData: function(data) {
    for (var i in data) {
      feature = data[i];
      if ((this.browser.cnv.gainloss == 'gain' && parseFloat(feature.mean_ratio) > 0) ||
        (this.browser.cnv.gainloss == 'loss' && parseFloat(feature.mean_ratio) < 0)) {
          feature.label = feature.patient_id;
          feature.name = feature.patient_id;
          this.insertFeature(feature);
        }
    }
  },
  insertFeature: function(a) {
    a.color = 0 < a.mean_ratio ?
      "#0052FF" : "#FF2F00";
    a.label = "number" === typeof a.patient_id ? a.patient_id.toString() : a.patient_id;
    this.base(a)
  },
  populateMenu: function(a, b) {
    var c = {},
    d = [
      ["title", "(" + this.browser.chr + ":" + a.start + "-" + a.end + ")" + (0 < a.mean_ratio ? "Dup" : "Del")],
      ["Patient", a.patient_id ? '<a target="_blank" href="https://decipher.sanger.ac.uk/patient/' + a.patient_id + "#genotype/cnv/" + a.id + '/browser">' + a.patient_id + "</a>" : '-'],
      ["Length", a.end - a.start + 1 + " bp"],
      ["Location", this.browser.chr + ":" + a.start +
        "-" + a.end
      ],
      ["Mean ratio", a.mean_ratio],
      ["Inheritance", a.inheritance],
      ["Pathogenicity", a.pathogenicity],
      ["Chr_sex", a.chr_sex],
      ["Phenotypes", a.phenotypes],
    ],
    f;
    for (f in d) "undefined" !== typeof d[f][1] && (c[d[f][0]] = d[f][1]);
    return $.extend(c, b)
  }
});
