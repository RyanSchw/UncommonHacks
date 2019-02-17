var BUTTON_COL;

class Button {
    constructor(x, y, w, h, func){
        this.x = x;
        this.y = y;
        this.w = w;
        this.h = h;
        this.func = func;

        this.pressed = false;

        BUTTON_COL = color(237, 149, 229);
    }

    draw(){
        push();
        console.log(this.pressed);

        if (this.pressed){fill(BUTTON_COL);} 
        else {fill(BACKGROUND_COL);}

        strokeWeight(10);
        stroke(BUTTON_COL);
        //fill(BACKGROUND_COL);
        rectMode(CORNER);
        rect(this.x, this.y, this.w, this.y+this.h);

        //console.log([this.x, this.y, this.x+this.w, this.y+this.h]);

        // if (this.pressed){fill(BUTTON_COL);} 
        // else {fill('black');}

        fill('black');
        textAlign(CENTER, CENTER);
        noStroke();
        textSize(BUTTON_HEIGHT);
        text("Select Check Points", this.x+this.w/2, this.y+this.h/2 + 10);
        pop();
    }

    mouseClicked(){
        if (mouseX > this.x && mouseX < this.x + this.w
            && mouseY > this.y && mouseY < this.y + this.h){
                this.func();
                this.pressed = !this.pressed;
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