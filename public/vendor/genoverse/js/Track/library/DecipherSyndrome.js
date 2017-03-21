Genoverse.Track.DecipherSyndrome = Genoverse.Track.extend({
  id    : 'syndrome',
  name  : 'Decipher Syndrome',
  category  : 'Decipher Syndrome',
  info      : 'Decipher Syndrome',
  tags      : ['decipher', 'syndrome'],
  url       : '/api/annodb/deciphersyndrome?chr=__CHR__&start=__START__&end=__END__',
  height    : 20,
  autoheight  : true,
  hideEmpty   : false,
  featureHeight : 6,
  labels        : true,
  repeatLabels  : true,
  bump          : true,
  parseData     : function(data) {
    for (var i in data) {
      feature = data[i];
      feature.label = feature.short_description;
      feature.name = feature.label;
      this.insertFeature(feature);
    }
  },
  setFeatureColor : function(feature) {
    feature.color = feature.labelColor = 2 < feature.copy_number ? '#0052FF' : '#FF2F00';
  },
  populateMenu    : function(feature, extra) {
    var data = {
      title: '<a target="_blank" href="https://decipher.sanger.ac.uk/syndrome/' + feature.syndrome_id + '#overview">' + feature.name + '</a>',
      'Location'   : 'chr' + feature.chr + ':' + feature.start + '-' + feature.end,
      'Copy Number': feature.copy_number
    };
    return $.extend(data, extra);
  }
});
