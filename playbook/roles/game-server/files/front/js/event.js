//const m_login       = "ゲームにログインしてください";
//const m_create      = "アカウントをさくせいします";
//const m_input       = "ID,Password,Nicknameを入力してください";
//const m_start       = 'ぼうけんをはじめる';
//const m_select      = 'メニューから行動を選択してください。');
//const m_back        = 'メニューに戻ります。');
//const m_lackstamina = "スタミナが不足しています。     ";
//const m_created     = "アカウントをさくせいしました";
const m_event_login       = "Login";
const m_event_create      = "Create account.";
const m_event_input       = "Please enter your ID,Password and Nickname.";
const m_event_start       = 'Start playing the game.';
const m_event_select      = 'Command?';
const m_event_back        = 'Return to menu.';
const m_event_lackstamina = "Lack of stamina.";
const m_event_created     = "Account created.";
//
//// イベントハンドラの定義
function showAlert(e) {
    console.log(e);
    alert('clicked(taped)');
}


function doCancelCreate(){
    login2Txt.text = "";

    openingContainer.addChild(loginButton);
    openingContainer.addChild(createButton);
    nickname.alpha = 0;

    //loginTxt.text = "ゲームにログインしてください";
    loginTxt.text = m_event_login;
    cancelButton  = openingContainer.removeChild(cancelButton);    
    create2Button = openingContainer.removeChild(create2Button);

}

function doCreateAccount(){    
    loginButton  = openingContainer.removeChild(loginButton);
    createButton = openingContainer.removeChild(createButton);
    openingContainer.addChild(create2Button);
    openingContainer.addChild(cancelButton);
    nickname.alpha = 1;

    //loginTxt.text = "アカウントをさくせいします";
    //login2Txt.text = "ID,Password,Nicknameを入力してください";
    loginTxt.text = m_event_create;
    login2Txt.text = m_event_input;
}

function uploadFile(){
    let input = document.getElementById('file');
    input.click();
}

function doOpening(e){
    player();
    console.log(e);
    
    //pixiSound.play('title');
    loginButton.off('pointertap', doOpening);
    loginButton.alpha = 0;
    loginButton.buttonMode = false;
    loginButton.interactive = false;

    createButton.off('pointertap', doCreateAccount);
    createButton.alpha = 0;
    createButton.buttonMode = false;
    createButton.interactive = false;

    // read title banner
    openingContainer.addChild(title);

    // action
    TweenMax.to(title, 2.0, 
        {   
            pixi: { 
                y: title.y + app.screen.height / 6 * 2, 
            },
            ease: Power0.easeNone, 
            repeat: 0,
            //yoyo: true
        }
    );

    let changeScean = () => {
        //startTxt.text = 'ぼうけんをはじめる';
        startTxt.text = m_event_start;
        startTxt.alpha = 1;
        startTxt.interactive = true;
        startTxt.buttonMode = true;
        startTxt.on('pointertap', jumpModeMenu);
        copyrightTxt.alpha = 1;
        openingTimer = setInterval(blinkElement, 700);
    }

    let blinkElement = () => {
        if(openingContainer.getChildByName('clickToStart') !== null ){
            let elm = openingContainer.getChildByName('clickToStart');
            if(startTxt.alpha === 0){
                elm.alpha = 1;
            } else {
                elm.alpha = 0;
            }
        }
    }

    setTimeout(changeScean, 2000);
}

function doCreate(){
    new_user(uid.text,passwd.text,nickname.text);
    let nextx = () => {
        let res = JSON.parse(sessionStorage.getItem("new_user"));
        if( res.result === "ok" ){
            //login2Txt.text = "アカウントをさくせいしました";
            login2Txt.text = m_event_created;
            sessionStorage.removeItem("new_user");
            setTimeout(doCancelCreate, 1000);
        } else {
            console.log(res.msg);
            login2Txt.text = res.msg;
            sessionStorage.removeItem("new_user");
        }
    }
    setTimeout(nextx, 2000);
}

function doLogin(){
    login(uid.text,passwd.text);
    let next = () => {
        let res = JSON.parse(sessionStorage.getItem("login"));
        //console.log(res);
        let sessid = getCookieVal("session_id");
        if( res.result === "ok" && sessid !== undefined){
            // check the user
            loginTxt.alpha = 0;
            loginButton.alpha = 0;
            uid.alpha = 0;
            passwd.alpha = 0;
            sessionStorage.removeItem("login");
            login2Txt.text = "";
            doOpening();
        } else {
            console.log(res.msg);
            login2Txt.text = res.msg;
            sessionStorage.removeItem("login");
        }
    }
    setTimeout(next, 2000);
}

function doGatyaToMenu(){

    let goToMenu = () => {
        gachaContainer = app.stage.removeChild(gachaContainer);
        modeMenu();
        clearMessage(menu);
        //setMessage(menu, 'メニューから行動を選択してください。');
        setMessage(menu, m_event_select);
    };

    clearMessage(gacha);
    //setMessage(gacha, 'メニューに戻ります。');
    setMessage(gacha, m_event_back);
    setTimeout(goToMenu, 800);
}


function doStaminaToMenu(){

    let goToMenu = () => {
        staminaContainer = app.stage.removeChild(staminaContainer);
        modeMenu();
        clearMessage(menu);
        //setMessage(menu, 'メニューから行動を選択してください。');
        setMessage(menu, m_event_select);
    };

    clearMessage(stamina);
    //setMessage(stamina, 'メニューに戻ります。');
    setMessage(stamina, m_event_back);
    setTimeout(goToMenu, 800);
}

function doPstatToMenu(){

    let goToMenu = () => {
        pstatContainer = app.stage.removeChild(pstatContainer);
        modeMenu();
        clearMessage(menu);
        //setMessage(menu, 'メニューから行動を選択してください。');
        setMessage(menu, m_event_select);
    };

    setTimeout(goToMenu, 500);
}

function doChargeToMenu(){

    let goToMenu = () => {
        chargeContainer = app.stage.removeChild(chargeContainer);
        modeMenu();
        clearMessage(menu);
        //setMessage(menu, 'メニューから行動を選択してください。');
        setMessage(menu, m_event_select);
    };

    clearMessage(charge);
    //setMessage(charge, 'メニューに戻ります。');
    setMessage(charge, m_event_back);
    setTimeout(goToMenu, 800);
}

function courseToMenu(msg=""){
    if(typeof(msg) === "object"){
        msg = "";
    }

    let goToMenu = () => {
        courseContainer = app.stage.removeChild(courseContainer);
        modeMenu();
        menuContainer.alpha = 1;
        clearMessage(battle);
        //setMessage(menu, msg + 'メニューから行動を選択してください。');
        setMessage(menu, msg + " " + m_event_select);
    };

    setTimeout(goToMenu, 800);
}

function coursepostJudgeMsg(res=""){
    let msg = "";
    console.log(res.msg);
    if(res.msg === "You lacking stamina.") {
        //msg = "スタミナが不足しています。     ";
        msg = m_event_lackstamina;
    } else {
        msg = res.msg;
    }
    return msg;
}

function courseToBattle1(){
    sessionStorage.setItem("course", 1);
    coursepost(1);

    let goToBattle = () => {
        let res = JSON.parse(sessionStorage.getItem('coursepost'));
        if(res.result !== "ng"){
            sra1.alpha = 1;
            courseContainer = app.stage.removeChild(courseContainer);
            modeBattle(1);
        } else {
            // NG
            let msg = coursepostJudgeMsg(res);
            courseToMenu(msg);
        }
    };

    setTimeout(goToBattle, 1000);
}

function courseToBattle2(){
    sessionStorage.setItem("course", 2);
    coursepost(2);

    let goToBattle = () => {
        let res = JSON.parse(sessionStorage.getItem('coursepost'));
        if(res.result !== "ng"){
            sra2.alpha = 1;
            courseContainer = app.stage.removeChild(courseContainer);
            modeBattle(2);
        } else {
            // NG
            let msg = coursepostJudgeMsg(res);
            courseToMenu(msg);
        }
    };

    setTimeout(goToBattle, 1000);
}

function courseToBattle3(){
    sessionStorage.setItem("course", 3);
    coursepost(3);

    let goToBattle = () => {
        let res = JSON.parse(sessionStorage.getItem('coursepost'));
        if(res.result !== "ng"){
            sra3.alpha = 1;
            courseContainer = app.stage.removeChild(courseContainer);
            modeBattle(3);
        } else {
            // NG
            let msg = coursepostJudgeMsg(res);
            courseToMenu(msg);
        }
    };

    setTimeout(goToBattle, 800);
}

function courseToBattle4(){
    sessionStorage.setItem("course", 4);
    coursepost(4);

    let goToBattle = () => {
        let res = JSON.parse(sessionStorage.getItem('coursepost'));
        if(res.result !== "ng"){
            sra4.alpha = 1;
            courseContainer = app.stage.removeChild(courseContainer);
            modeBattle(4);
        } else {
            // NG
            let msg = coursepostJudgeMsg(res);
            courseToMenu(msg);
        }
    };

    setTimeout(goToBattle, 800);
}

function courseToBattle5(){
    sessionStorage.setItem("course", 5);
    coursepost(5);

    let goToBattle = () => {
        let res = JSON.parse(sessionStorage.getItem('coursepost'));
        if(res.result !== "ng"){
            sra5.alpha = 1;
            courseContainer = app.stage.removeChild(courseContainer);
            modeBattle(5);
        } else {
            // NG
            let msg = coursepostJudgeMsg(res);
            courseToMenu(msg);
        }
    };

    setTimeout(goToBattle, 800);
}
