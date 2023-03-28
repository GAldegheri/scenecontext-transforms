
var LeftRect =
{ obj_type: 'rect',
  startX: function()
  {
    return -img_size[0]/2-300;
  },
  startY: 0,
  origin_center: true,
  width: 600,
  height: 1000,
  fill_color: 'grey'
};

var RightRect =
{
  obj_type: 'rect',
  startX: function()
  {
    return img_size[0]/2+300;
  },
  startY: 0,
  origin_center: true,
  width: 600,
  height: 1000,
  fill_color: 'grey'
};

var BottomRect =
{
  obj_type: 'rect',
  startX: 0,
  startY: function()
  {
    return img_size[1]/2+300;
  },
  origin_center: true,
  width: 2000,
  height: 600,
  fill_color: 'grey'
};

var TopRect =
{
  obj_type: 'rect',
  startX: 0,
  startY: function()
  {
    return -img_size[1]/2-300;
  },
  origin_center: true,
  width: 2000,
  height: 600,
  fill_color: 'grey'
};
