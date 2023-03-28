var GA_utils = (function() {

  var my = {};

  my.cartesian = function*(head, ...tail)
  {
    // Courtesy of:
    // https://stackoverflow.com/questions/4331092/finding-all-combinations-cartesian-product-of-javascript-array-values
    let remainder = tail.length ? my.cartesian(...tail) : [[]];
    for (let r of remainder) for (let h of head) yield [h, ...r];
  }

  my.reparray = function(arr, n)
  {
    var a = [];
    while (a.length < arr.length * n) a = a.concat(JSON.parse(JSON.stringify(arr))); // deep copy of array
    return a;
  }

  my.create_named_array = function(arr, col_names)
  {
    var named_arr = [];
    for (var i = 0; i < arr.length; i++)
    {
      var thisrow = {};
      for (var j = 0; j < col_names.length; j++)
      {
        thisrow[col_names[j]] = arr[i][j];
      }
      named_arr = named_arr.concat(thisrow);
    }
    return named_arr;
  }

  my.range = function(start, end)
  {
      return (new Array(end - start + 1)).fill(undefined).map((_, i) => i + start);
  }

  my.shuffle = function(array)
  {
    // Courtesy of:
    // https://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array
    var currentIndex = array.length, temporaryValue, randomIndex;

    // While there remain elements to shuffle...
    while (0 !== currentIndex) {

      // Pick a remaining element...
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex -= 1;

      // And swap it with the current element.
      temporaryValue = array[currentIndex];
      array[currentIndex] = array[randomIndex];
      array[randomIndex] = temporaryValue;
    }

    return array;
  }

  my.double_shuffle = function(array1, array2)
  {
    // Courtesy of
    // https://stackoverflow.com/questions/18194745/shuffle-multiple-javascript-arrays-in-the-same-way
    var index = array1.length;
    var rnd, tmp1, tmp2;

    while (index)
    {
      rnd = Math.floor(Math.random() * index);
      index -= 1;
      tmp1 = array1[index];
      tmp2 = array2[index];
      array1[index] = array1[rnd];
      array2[index] = array2[rnd];
      array1[rnd] = tmp1;
      array2[rnd] = tmp2;
    }

  }

  my.randn_bm = function()
  {
    // Standard Normal variate using Box-Muller transform.
    // Courtesy of https://stackoverflow.com/a/36481059
    var u = 0, v = 0;
    while(u === 0) u = Math.random(); //Converting [0,1) to (0,1)
    while(v === 0) v = Math.random();
    return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
  }

  my.range = function(start, stop, step)
  {
    // courtesy of https://stackoverflow.com/a/8273091
    if (typeof stop == 'undefined') {
        // one param defined
        stop = start;
        start = 0;
    }

    if (typeof step == 'undefined') {
        step = 1;
    }

    if ((step > 0 && start >= stop) || (step < 0 && start <= stop)) {
        return [];
    }

    var result = [];
    for (var i = start; step > 0 ? i < stop : i > stop; i += step) {
        result.push(i);
    }

    return result;
  }

  my.split = function(left, right, parts)
  {
    // courtesy of https://stackoverflow.com/a/51250825
    var result = [];
    var delta = (right - left) / (parts - 1);
    while (left < right) {
        result.push(left);
        left += delta;
    }
    if (result.length >= parts)
    { result.pop(); }
    result.push(right);
    return result;
  }

  return my;
})();
