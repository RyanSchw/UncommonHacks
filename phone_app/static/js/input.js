class Button {
    constructor(text, x, y, w, h, func){
        this.text = text;
        this.x = x;
        this.y = y;
        this.w = w;
        this.h = h;
        this.func = func;

        this.pressed = false;
    }

    draw(){
        push();

        if (this.pressed){fill(BUTTON_COL);} 
        else {fill(BACKGROUND_COL);}

        strokeWeight(10);
        stroke(BUTTON_COL);
        //fill(BACKGROUND_COL);
        rectMode(CORNER);
        rect(this.x, this.y, this.w, this.h);

        //console.log([this.x, this.y, this.x+this.w, this.y+this.h]);

        if (this.pressed){fill('white');} 
        else {fill(BUTTON_COL);}

        textAlign(CENTER, CENTER);
        noStroke();
        textSize(BUTTON_HEIGHT * 0.4);
        text(this.text, this.x+this.w/2, this.y+this.h/2);
        pop();
    }

    mouseClicked(){
        if (mouseX > this.x && mouseX < this.x + this.w
            && mouseY > this.y && mouseY < this.y + this.h){
                this.func();
                //this.pressed = !this.pressed;
        }
    }
}

var cp_button_onclick = function(){
    if(!cp_toggle_button.pressed){
        // Button turned on
        cp_toggle_button.pressed = true;
    } else {
        // Button turned off
        cp_toggle_button.pressed = false;

        cps = checkpoints_to_json();
        send_checkpoints(cps);
    }
}

function checkpoints_to_json(){
    conv = {"checkpoints": []};
    checkpoints.forEach(function(cp){
		conv.checkpoints.push(cp.to_json());
    });
    
    return conv;
}

function send_checkpoints(data){
    socket.emit('get_checkpoints', {
        data: JSON.stringify(data)
    });
}

var record_button_onclick = function(){
    console.log('Record pressed');
	if(!record_button.pressed){
        // Button turned on
        record_button.pressed = true;

        req_rec(true);
    } else {
        // Button turned off
        record_button.pressed = false;
        req_rec(false);
    }
}

function req_rec(on){
    socket.emit('req-rec', {
        record: on
    });
}

var toggle_button_onclick = function(){
	
}

var handle_checkpoint_click = function(){
	if (cp_toggle_button.pressed && mouseX < LINE_POS_X){
		if(checkpoints.length == 0 || checkpoints[checkpoints.length - 1].placed){
			checkpoints.push(new CheckPoint(mouseX, mouseY));
		} else {
			checkpoints[checkpoints.length - 1].place(mouseX, mouseY);
		}
	}
}

class CheckPoint {
    constructor(x1, y1){
        this.x1 = x1;
        this.y1 = y1;
        this.x2 = 0;
        this.y2 = 0;

        this.placed = false;
    }

    to_json(){
        return {"x1": this.x1/LINE_POS_X, "y1": this.y1/windowHeight, "x2": this.x2/LINE_POS_X, "y2": this.y2/windowHeight};
    }

    draw(){
        push();
        strokeWeight(3);
        if(!this.placed){
            line(this.x1, this.y1, mouseX, mouseY);
        } else {
            line(this.x1, this.y1, this.x2, this.y2);
        }
        pop();
    }

    place(x2, y2){
        this.x2 = x2;
        this.y2 = y2;
        this.placed = true;
    }
}