var NUM_ELEMENTS = 400;

class Sample {
    constructor(pos, vel, acc, time){
        this.pos = pos;
        this.vel = vel;
        this.acc = acc;
        this.time = time;
    }
}

function parse_samples(data) {
    parsed = JSON.parse(data).samples;

    var samples = [];
    for(var i = 0; i < parsed.length; i++){
        p = createVector(parsed[i].pos.x, parsed[i].pos.y);
        v = createVector(parsed[i].vel.x, parsed[i].vel.y);
        a = createVector(parsed[i].acc.x, parsed[i].acc.y);
        t = parsed[i].time;
        samples.push(new Sample(p, v, a, t));
    }

    return samples;
}

function draw_data(samples, rad){
    push();
    colorMode(HSB);
    noStroke();
    for(var i = 0; i < samples.length; i++){
        fill(color((1 - samples[i].vel.mag() / 20) * 255, 200, 90))
        circ_x = (DISPLAY_SIZE - PADDING_PIX) * samples[i].pos.x + PADDING_PIX
        circ_y = (DISPLAY_SIZE - 2*PADDING_PIX) * samples[i].pos.y + PADDING_PIX
        circle(circ_x, circ_y, rad);
    }
    textSize(50);
    colorMode(RGB);
    fill(BUTTON_COL)
    if(cur_run != 0)
        text("Checkpoint: " + cur_run, 10, 50);
    else
    text("Checkpoint: Full Track", 10, 50);
    pop();
}

function gen_rand_samples(n){
    var samples = [];

    for (i = 0; i < n; i++){
        p = vec_abs(createVector(Math.random(), Math.random()));
        v = vec_abs(createVector(Math.random(), Math.random()));
        a = vec_abs(createVector(Math.random(), Math.random()));
        t = Math.random();
        samples.push(new Sample(p, v, a, t));
    }

    return samples;
}

function vec_abs(v){
    return createVector(Math.abs(v.x), Math.abs(v.y));
}

class Stats{
    constructor(x, y, w, h){
        this.x = x;
        this.y = y;
        this.w = w;
        this.h = h;
    }

    draw(){
        var text_height = BUTTON_HEIGHT * 0.3;
        fill(BUTTON_COL);
        textAlign(LEFT);
        noStroke();
        textSize(text_height);
        text("Statistics:", this.x, this.y);

        if(samples[samples.length-1])
            text("Lap time: " + samples[samples.length-1].time, this.x, this.y + text_height);
    }
}