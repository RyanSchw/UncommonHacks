// Variables
var x, y;
var cp_toggle_button;
var record_button;
var toggle_button;
var checkpoints = [];
var socket;
var samples = [];

// Constants
var DISPLAY_SIZE;
var BACKGROUND_COL;
var PADDING_RATIO = 0.02;
var PADDING_PIX;
var DOT_RAD = 7;
var LINE_POS_X;
var BUTTON_HEIGHT;

function setup() {
	// put setup code here
	createCanvas(windowWidth, windowHeight);

	socket = io.connect('https://' + document.domain + ':' + location.port + '/sock');

	var received_data;
	socket.on('data_vis', function (msg) {
		samples = parse_samples(msg.data);
	});

	socket.on('summary', function (msg) {
		console.log(msg)
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
	toggle_button.mouseClicked();
}

function keyPressed(){
	if(keyCode == ESCAPE && !checkpoints[checkpoints.length - 1].placed){
		checkpoints.pop();
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
		LINE_POS_X + PADDING_PIX, PADDING_PIX + 2*BUTTON_HEIGHT, BUTTON_WIDTH / 2, BUTTON_HEIGHT, record_button_onclick);
	toggle_button = new Button("Toggle", 
		LINE_POS_X + PADDING_PIX + BUTTON_WIDTH/2, PADDING_PIX + 2*BUTTON_HEIGHT, 
		BUTTON_WIDTH / 2, BUTTON_HEIGHT, toggle_button_onclick);
}

function draw_dash(){
	push();
	strokeWeight(5);
	line(LINE_POS_X, 0, LINE_POS_X, DISPLAY_SIZE);
	cp_toggle_button.draw();
	record_button.draw();
	toggle_button.draw();

	//cp_toggle_button.draw();
	pop();
}