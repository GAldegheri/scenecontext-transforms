
const img_offset = 0;

var expl_img_indx = 0;
var ready = 0;

var samediff_expl_rot = [
  { img: [ProbeDir, `/Scene1_60_0030_-0.5.png`].join(``),
    prompt: [`<strong style = "position:absolute;left:calc(50%);top:calc(50%);transform:translateX(-50%)`,
           `translateY(-300px); font-size: 30px; background-color: white;`,
           `line-height:1.4">And then the object will reappear!</strong>`].join(``)},
  { img: [ProbeDir, `/Scene1_60_0030_-0.5.png`].join(``),
    prompt: [`<strong style = "position:absolute;left:calc(50%);top:calc(50%);transform:translateX(-50%)`,
           `translateY(-300px); font-size: 30px; background-color: white;`,
           `line-height:1.4">After reappearing...</strong>`].join(``)},
  { img: [ProbeDir, `/Scene1_60_0030_8.0.png`].join(``),
    prompt: [`<strong style = "position:absolute;left:calc(50%);top:calc(50%);`,
             `transform:translateX(-50%) translateY(-300px); font-size: 30px;`,
             `background-color: white; line-height:1.4">It will change on half the trials!</strong>`].join(``)},
  { img: [ProbeDir, `/Scene1_60_0030_8.0.png`].join(``),
    prompt: [`<strong style = "position:absolute;left:calc(50%);top:calc(50%);`,
             `transform:translateX(-50%) translateY(-300px); font-size: 30px;`,
             `background-color: white; line-height:1.4">In this case, it did change.</strong>`].join(``)},
  { img: [StimDir, `/Scene2_0_0090.png`].join(``),
    prompt: [`<strong style = "position:absolute;left:calc(50%);top:calc(50%);`,
            `transform:translateX(-50%) translateY(-300px); font-size: 30px;`,
            `background-color: white; line-height:1.4">Here it did NOT change.</strong>`].join(``)}
];

// -----------------------------------------------------------------------------
// Normal rotation sequence
// -----------------------------------------------------------------------------

var allviews_expl_1 = [
  {img: [StimDir, `/Scene1_60_0000.png`].join(``),
  prompt: [`<strong style = "position:absolute;left:calc(50%);top:calc(50%);`,
           `transform:translateX(-50%) translateY(-300px); font-size: 30px;`,
           `background-color: white; line-height:1.4">You will see scenes like these,<br>`,
           `with a main object in the center (a sofa or a bed):</strong>`].join(``)},
  {img: [StimDir, `/Scene1_60_0010.png`].join(``),
  prompt: [`<strong style = "position:absolute;left:calc(50%);top:calc(50%);`,
          `transform:translateX(-50%) translateY(-300px); font-size: 30px;`,
          `background-color: white; line-height:1.4">The scenes will rotate...</strong>`].join(``)},
  {img: [StimDir, `/Scene1_60_0015.png`].join(``),
  prompt: [`<strong style = "position:absolute;left:calc(50%);top:calc(50%);`,
          `transform:translateX(-50%) translateY(-300px); font-size: 30px;`,
          `background-color: white; line-height:1.4">`,
          `And at some point the object in the center will disappear.</strong>`].join(``)},
  {img: [StimDir, `/Scene1_60_0020.png`].join(``),
  prompt: [`<strong style = "position:absolute;left:calc(50%);top:calc(50%);transform:translateX(-50%)`,
           `translateY(-300px); font-size: 30px; background-color: white; line-height:1.4">`,
           `The scene will keep rotating...</strong>`].join(``)},
  {img: [StimDir, `/Scene1_60_0030.png`].join(``),
  prompt: [`<strong style = "position:absolute;left:calc(50%);top:calc(50%);transform:translateX(-50%)`,
           `translateY(-300px); font-size: 30px; background-color: white; line-height:1.4">And again...</strong>`].join(``)},
];

var allviews_expl_2 = [
  {img: [StimDir, `/Scene2_0_0000.png`].join(``),
   prompt: [`<strong style = "position:absolute;left:calc(50%);top:calc(50%);`,
            `transform:translateX(-50%) translateY(-300px); font-size: 30px;`,
            `background-color: white; line-height:1.4">Another example:</strong>`].join(``)},
  {img: [StimDir, `/Scene2_0_0010.png`].join(``),
   prompt: [`<strong style = "position:absolute;left:calc(50%);top:calc(50%);`,
           `transform:translateX(-50%) translateY(-300px); font-size: 30px;`,
           `background-color: white; line-height:1.4">The scene starts rotating...</strong>`].join(``)},
  {img: [StimDir, `/Scene2_0_0030.png`].join(``),
   prompt: [`<strong style = "position:absolute;left:calc(50%);top:calc(50%);`,
           `transform:translateX(-50%) translateY(-300px); font-size: 30px;`,
           `background-color: white; line-height:1.4">The object disappears...</strong>`].join(``)},
  {img: [StimDir, `/Scene2_0_0060.png`].join(``),
   prompt: [`<strong style = "position:absolute;left:calc(50%);top:calc(50%);`,
           `transform:translateX(-50%) translateY(-300px); font-size: 30px;`,
           `background-color: white; line-height:1.4">The scene continues rotating...</strong>`].join(``)},
  {img: [StimDir, `/Scene2_0_0090.png`].join(``),
   prompt: [`<strong style = "position:absolute;left:calc(50%);top:calc(50%);`,
           `transform:translateX(-50%) translateY(-300px); font-size: 30px;`,
           `background-color: white; line-height:1.4">...</strong>`].join(``)},
  {img: [StimDir, `/Scene2_0_0090.png`].join(``),
   prompt: [`<strong style = "position:absolute;left:calc(50%);top:calc(50%);`,
           `transform:translateX(-50%) translateY(-300px); font-size: 30px;`,
           `background-color: white; line-height:1.4">...and the object reappears!</strong>`].join(``)}
];

// -----------------------------------------------------------------------------

const explanation_images = [
  ...allviews_expl_1,
  // -------------
  samediff_expl_rot[0],
  samediff_expl_rot[1],
  samediff_expl_rot[2],
  samediff_expl_rot[3],
  // -------------
  ...allviews_expl_2,
  // -------------
  samediff_expl_rot[4]
];

var preload_expl = {
  type: 'preload',
  images: function()
  {
    preloadimgs = [];
    for (var i = 0; i < explanation_images.length; i++)
    { preloadimgs.push(explanation_images[i].img); }
    return preloadimgs;
  },
  show_progress_bar: false,
  show_detailed_errors: true
};

var initial_text = {
  timeline: [
    {
      type: 'html-button-response',
      stimulus: [`<strong style = "font-size: 30px; line-height:1.4">Hi, and welcome to the experiment!<br><br>`,
                `Please sit comfortably,<br>`,
                `keep about an arm's length distance from the screen,<br>`,
                `close other applications, turn off your phone and avoid distractions.</strong>`].join(``),
      choices: ['Continue >'],
      margin_vertical: '50px'
    },
    {
      type: 'html-button-response',
      stimulus: [`<strong style = "font-size: 30px; line-height:1.4">The experiment will last around 30 minutes.<br>`,
                `There will be short blocks with breaks in between.</strong>`].join(``),
      choices: ['Continue >'],
      margin_vertical: '50px'
    },
    {
      type: 'html-button-response',
      stimulus: function(){
        return [`<strong style = "font-size: 30px; line-height:1.4">You will see a sequence of images,<br>`,
                `showing rooms with a bed or a sofa in the middle.<br><br>`,
                `These scenes' viewpoint will change, and the bed/sofa will disappear for some time.<br>`,
                `Then it will reappear, and on half of trials, it will change a little bit.<br>`,
                `You will have to indicate if the object changed or not.<br><br>`,
                `Now I will show you the stimuli and explain it more clearly.<br>`,
                `Please feel free to navigate back and forth to look at the images<br>`,
                `and make sure you understand everything!</strong>`].join(``); },
      choices: ['Continue >'],
      margin_vertical: '50px'
    }
  ]
};

var fix_dot_expl =
{
  obj_type: 'circle',
  startX: 0,
  startY: function() {return 150 + img_offset;},
  radius: 5,
  origin_center: true,
  line_color: 'black',
  fill_color: 'white'
};

var fix_instruction =
{
  type: 'psychophysics',
  canvas_height: 500,
  prompt: [`<strong style = "position:absolute;left:calc(50%);top:calc(50%);`,
           `transform:translateX(-50%) translateY(-150px); font-size: 30px;`,
           `line-height:1.4">Please keep your eyes on the fixation dot during the experiment.</strong>`].join(``),
  button_choices: ['Continue >'],
  response_type: 'button',
  stimuli: [fix_dot_expl]
};

var explanation_sequence =
{
  timeline: [
    {
      type: 'psychophysics',
      canvas_height: 700,
      prompt: function(){ return explanation_images[expl_img_indx].prompt; },
      button_choices: function(){
         if (expl_img_indx==0) { return ['Continue >']; }
         else {return ['< Back', 'Continue >']; }
       },
      response_type: 'button',
      stimuli: [
        {obj_type: 'image',
        file: function() { return explanation_images[expl_img_indx].img; },
        startY: img_offset,
        origin_center: true,
        width: img_size[0],
        height: img_size[1]},
        { // occluder
          obj_type: 'rect',
          origin_center: true,
          startX: 0,
          startY: function()
          {
            var whichview = 0;
            var y_min = box_coords[0][whichview][1];
            var height = box_coords[0][whichview][3];
            return -(img_size[1]/2 - y_min) + height/2;
          },
          origin_center: true,
          width: function()
          {
            var whichview = 0;
            var thiswidth = box_coords[0][whichview][2] + x_margin;
            var occlviews = [2, 4, 11, 13];
            if (expl_img_indx < occlviews[0] || (expl_img_indx > occlviews[1] && expl_img_indx < occlviews[2]) || expl_img_indx > occlviews[3])
            { return 0; } else
            { return thiswidth; }
          },
          height: function()
          {
            var thisheight = box_coords[0][0][3] + y_margin;
            return thisheight;
          },
          fill_color: 'grey',
        },
        fix_dot_expl
      ],
      on_finish: function(data) {
        if (data.button_pressed==0)
        { if (expl_img_indx==0)
          {expl_img_indx += 1;} else {expl_img_indx -= 1;} }
        else {
          { expl_img_indx += 1; }
        }
      }
    }
  ],
  loop_function: function(data){
    if(expl_img_indx < explanation_images.length){
      return true;
    } else {
      return false;
    }
  }
};

var pre_anim_text = {
  timeline: [
    {
      type: 'html-button-response',
      stimulus: function(){
                return [`<strong style = "font-size: 30px; line-height:1.4">`,
                `Your task is to report whether the object changes,<br>`,
                `AFTER the object has reappeared.<br><br>`,
                `However, it's IMPORTANT for the experiment<br>that you look at the whole sequence.</strong>`].join(``);},
      choices: ['Continue >'],
      margin_vertical: '50px'
    },
    {
      type: 'html-button-response',
      stimulus: function(){
                return [`<strong style = "font-size: 30px; line-height:1.4">`,
                `Press the F key for NO CHANGE, and the J key for CHANGE.<br>`,
                `Try to be as accurate and fast as possible.</strong>`].join(``);},
      choices: ['Continue >'],
      margin_vertical: '50px'
    },
    {
      type: 'html-button-response',
      stimulus: function(){
                return [`<strong style = "font-size: 30px; line-height:1.4">`,
                `Now, you will see a summary of what change and no change look like.</strong>`].join(``);},
      choices: ['Continue >'],
      margin_vertical: '50px'
    }
  ]
};

var animation_backandforth_same = {
  timeline: [
  {
    type: 'psychophysics',
    prompt: [`<strong style = "position:absolute;left:calc(50%);top:calc(50%);`,
            `transform:translateX(-50%) translateY(-300px); font-size: 30px;`,
            `background-color: white; line-height:1.4">NO CHANGE<br>(Press F)</strong>`].join(``),
    stimuli: [
      {obj_type: 'image',
       file: 'Renders_6views_optim/Scene1_60_0030.png',
       show_start_time: 200,
       show_end_time: 700},
      {obj_type: 'image',
       file: 'Renders_6views_optim/Scene1_60_0030.png',
       show_start_time: 800,
       show_end_time: 1300},
       fix_dot_expl
    ],
    trial_duration: 2100,
    choices: jsPsych.NO_KEYS
  }],
  repetitions: 4
};

var flip_rot = [
  {obj_type: 'image',
   file: 'Renders_6views_optim/Scene4_60_0030.png',
   show_start_time: 200,
   show_end_time: 700},
  {obj_type: 'image',
   file: 'Rotate_6views_optim/Scene4_60_0030_-7.0.png',
   show_start_time: 800,
   show_end_time: 1300},
   fix_dot_expl
];

var animation_backandforth_diff = {
  timeline: [
    {
      type: 'psychophysics',
      prompt: [`<strong style = "position:absolute;left:calc(50%);top:calc(50%);`,
              `transform:translateX(-50%) translateY(-300px); font-size: 30px;`,
              `background-color: white; line-height:1.4">CHANGE<br>(Press J)</strong>`].join(``),
      stimuli: flip_rot,
      trial_duration: 2100,
      choices: jsPsych.NO_KEYS
    }
  ],
  repetitions: 4
};

var all_clear =
{
  type: 'html-button-response',
  stimulus: [`<strong style = "font-size: 30px; line-height:1.4">All clear?</strong>`].join(``),
  choices: ['< No, please show me again', 'Yeah! Ready to continue >'],
  margin_vertical: '50px',
  on_finish: function(data) {
    if (data.response==1)
    { ready = 1; } else { ready = 0; }
  }
};

var training_msg =
{
  type: 'html-button-response',
  stimulus: [`<strong style = "font-size: 30px; line-height:1.4">Great, now you will have a short training session!<br><br>`,
             `In the experiment, the final objects will be shown very fast!<br>`,
             `So in the training session they will get gradually faster.<br><br>`,
             `After your response, the fixation dot will become<br>`,
             `<span style="color: rgb(0,255,0);">GREEN</span> for a correct response<br>`,
             `and <span style="color: rgb(255,0,0);">RED</span> for an incorrect response.</strong>`].join(``),
  choices: ['Continue >'],
  margin_vertical: '50px',
  on_finish: function(data) {
    if (data.response==1)
    { ready = 1; } else { ready = 0; }
  }
  };

var animation_sequence =
{
  timeline:
  [
    animation_backandforth_same,
    animation_backandforth_diff,
    all_clear
  ],
  loop_function: function(){
    return (ready==0);
  }
};

var whole_explanation = {
  timeline: [
    preload_expl, initial_text,
    explanation_sequence, pre_anim_text, animation_sequence,
    training_msg, fix_instruction
  ]
};
