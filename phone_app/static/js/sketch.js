// Variables
var x, y;
var cp_toggle_button;
var record_button;
var checkpoints = [];
var socket;
var samples = [];
var runs = [];
var cur_run = 0;
var stats;

// Constants
var DISPLAY_SIZE;
var BACKGROUND_COL;
var PADDING_RATIO = 0.02;
var PADDING_PIX;
var DOT_RAD = 7;
var LINE_POS_X;
var BUTTON_HEIGHT;
var BUTTON_COL;

function setup() {
	// put setup code here
	createCanvas(windowWidth, windowHeight);

	socket = io.connect('https://' + document.domain + ':' + location.port + '/sock');
	BUTTON_COL = color(40, 40, 40);

	var received_data;
    socket.on('data_vis', function (msg) {
        runs.append(parse_samples(msg.data));
    });

    socket.on('summary', function (msg) {
        console.log(msg['cps'])
        sample_lists = msg['cps']
        for(i in sample_lists) {
            console.log()
            runs.append(parse_samples(sample_lists[i]))
        }
        
    });

	draw_setup();
}

function draw() {
	// put drawing code here
	//draw_data(x, y, 5);
	background(BACKGROUND_COL);
	draw_data(samples, DOT_RAD);

	checkpoints.forEach(function(cp){
		cp.draw();
	});

	draw_dash();

}

function windowResized() {
	resizeCanvas(windowWidth, windowHeight);
	draw_setup();
}

function mousePressed(){
	handle_checkpoint_click();

	cp_toggle_button.mouseClicked();
	record_button.mouseClicked();
}

function keyPressed(){
	if(keyCode == ESCAPE && !checkpoints[checkpoints.length - 1].placed){
		checkpoints.pop();
	}

	if(keyCode == UP_ARROW){
		cur_run = (cur_run + 1) % (runs.length + 1);
		samples = runs[cur_run];
	}
	if(keyCode == DOWN_ARROW){
		cur_run = (cur_run - 1) % (runs.length + 1);
		samples = runs[cur_run];
	}
}

function draw_setup(){
	BACKGROUND_COL = color(200, 200, 200);
	background(BACKGROUND_COL);
	DISPLAY_SIZE = windowHeight;
	PADDING_PIX = DISPLAY_SIZE * PADDING_RATIO;
	LINE_POS_X = DISPLAY_SIZE + DOT_RAD + PADDING_PIX;
	BUTTON_WIDTH = windowWidth - LINE_POS_X - 2*PADDING_PIX;
	BUTTON_HEIGHT = DISPLAY_SIZE * 0.15;
	draw_data(samples, DOT_RAD);
	setup_dash();
	//cp_toggle_button = new Button(LINE_POS_X + PADDING_PIX, PADDING_PIX, BUTTON_WIDTH, BUTTON_HEIGHT, function(){});
	draw_dash();
}

var cp_button_func = function(){
	if (cp_toggle_button.pressed && mouseX < LINE_POS_X){
		if(checkpoints.length == 0 || checkpoints[checkpoints.length - 1].placed){
			checkpoints.push(new CheckPoint(mouseX, mouseY));
		} else {
			checkpoints[checkpoints.length - 1].place(mouseX, mouseY);
		}
	}
}

function setup_dash(){
	cp_toggle_button = new Button("Select Check Points", 
		LINE_POS_X + PADDING_PIX, PADDING_PIX, BUTTON_WIDTH, BUTTON_HEIGHT, cp_button_onclick);
	record_button = new Button("Record", 
		LINE_POS_X + PADDING_PIX, PADDING_PIX + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, record_button_onclick);

	stats = new Stats(LINE_POS_X + PADDING_PIX, 4*PADDING_PIX + 2*BUTTON_HEIGHT,
		BUTTON_WIDTH, windowHeight - (PADDING_PIX + 2*BUTTON_HEIGHT));
}

function draw_dash(){
	push();
	strokeWeight(5);
	fill(BUTTON_COL);
	line(LINE_POS_X, 0, LINE_POS_X, DISPLAY_SIZE);
	cp_toggle_button.draw();
	record_button.draw();
	stats.draw();

	//cp_toggle_button.draw();
	pop();
}