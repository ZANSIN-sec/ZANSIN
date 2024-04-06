
function getCookieVal(key){
    return ((document.cookie + ';').match(key + '=([^¥S;]*)')||[])[1];
}

function setStat() {
    let dmg = parseInt(sessionStorage.getItem("dmg"));
    if(dmg === undefined || dmg === null){
        dmg = 0;
    }
    statTxt1.text = pinfo.nick_name;
    statTxt2.text = "H: " + String(pinfo.armor_param + pinfo.max_hp - dmg);
    statTxt3.text = "A: " + String(pinfo.weapon_param + pinfo.max_str);
    statTxt4.text = "L: " + pinfo.level;
    statTxt5.text = "S: " + pinfo.stamina;
    statTxt6.text = "G: " + pinfo.gold;
}

function createMessage(m="",x=8,y=8) {
    let message =  new PIXI.Text(m, 
    { 
        fontFamily: 'PixelMplus10',
        fontSize: 20,
        fill : 0xffffff,      // font color    
    });
    message.x = x;
    message.y = y;
    return message;
}

function createIntMessage(m="",x=8,y=8) {
    let message =  new PIXI.Text(m, 
    { 
        fontFamily: 'PixelMplus10',
        fontSize: 20,
        fill : 0xffffff,      // font color
    });
    message.x = x;
    message.y = y;
    message.interactive = true;
    message.buttonMode = true;
    return message;
}


function clearMessage (t) {
    let cnt = 5;
    if(t === 'pstat'){
        cnt = 15;
    }
    for(i=0; i < cnt; i++){
        let elm = t + 'Message' + String(i+1);
        window[elm].text = "";
    }
}

function setMessageCustom (m1="",m2="",m3="", m4="", m5="") {
    message1.text = m1;
    message2.text = m2;
    message3.text = m3;
    message4.text = m4;
    message5.text = m5;
}

function setMessage (t="",m="") {
    //let charLenPerLine = 18;
    let charLenPerLine = 36; // for english
    let count = Array.from(m).length
    let lCount = Math.ceil(count / charLenPerLine);
    //let regex = /.{1,18}/gu;
    let regex = /.{1,36}/gu; // for english
    let lines = m.match(regex);
    clearMessage(t);
    for(i=0; i < lCount; i++){
        window[t+'Message'+String(i+1)].text = lines[i];
    }
}

function setActorWlkBattleMode(){
    actorWlk.x = app.screen.width - (app.screen.width / 3);
    actorWlk.y = app.screen.height / 2;
    actorWlk.anchor.set(0.5);
    actorWlk.animationSpeed = 0.05;
    actorWlk.zIndex = 20;
    actorWlk.scale.x = 2;
    actorWlk.scale.y = 2;
    actorWlk.alpha = 1;
    actorWlk.play();
}

function setActorWlkStatusMode(){
    actorWlk.x = app.screen.width / 2;
    actorWlk.y = app.screen.height / 2;
    actorWlk.anchor.set(0.5);
    actorWlk.animationSpeed = 0.05;
    actorWlk.zIndex = 20;
    actorWlk.scale.x = 3;
    actorWlk.scale.y = 3;
    actorWlk.alpha = 1;
}
