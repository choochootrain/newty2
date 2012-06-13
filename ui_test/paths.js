function get_path(url) {
  
}

function scale_array(arr, x, y) {
  var scaled = [];
  for(var i = 0; i < arr.length; i++) {
    scaled.push([arr[i][0] * x, arr[i][1] * y]);
  }
}

function drop_samples(arr, rate) {
  var sampled = [];
  for(var i = 0; i < arr.length; i+=rate) {
    sampled.push(arr[i]);
  }
  return sampled;
}

function average_samples(arr, rate) {
  var sampled = [];
  for(var i = 0; i < rate; i++) {
    sampled.push(arr[i]);
  }

  for(var i = rate; i < arr.length; i++) {
    var total = 0;
    for(var j = 0; j > -rate; j--) {
      total += arr[i + j][1];
    }
    sampled.push([arr[i][0], total/rate]);
  }
  return sampled;
}

function array_to_path(arr) {
  var path = "M0," + $('#container').height()/2;
  for(var i = 0; i < arr.length; i++) {
    path += "L" + arr[i][0] + "," + ($('#container').height()/2 - arr[i][1]);
  }
  return path;
}
