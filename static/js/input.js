$('#shower').slider({
   formatter: function(value) {
    console.log("inside");
    return 'current: ' + value;
   }
});

