var NUM_ELEMENTS = 400;

class Sample {
    constructor(pos, vel, acc, time){
        this.pos = pos;
        this.vel = vel;
        this.acc = acc;
        this.time = time;
    }
}

function get_samples() {
    return gen_rand_samples(NUM_ELEMENTS);
}

function draw_data(samples, rad){
    push();
    colorMode(HSB);
    //noStroke();
    for(var i = 0; i < samples.length; i++){
        fill(color((1 - samples[i].vel.mag()) * 255, 200, 90))
        circ_x = (DISPLAY_SIZE - PADDING_PIX) * samples[i].pos.x + PADDING_PIX
        circ_y = (DISPLAY_SIZE - 2*PADDING_PIX) * samples[i].pos.y + PADDING_PIX
        circle(circ_x, circ_y, rad);
    }
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