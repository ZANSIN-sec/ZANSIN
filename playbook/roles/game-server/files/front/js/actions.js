
//const m_battle_to           = "damage to the enemy.";
//const m_battle_from         = "damage from the enemy.";
//const m_battle_loose        = "敵に倒されてしまった・・・。";
//const m_battle_loose        = "敵を倒した。";
//const m_withdrowal_game     = "データを削除して退会します。本当によろしいですか？";
//const m_withdrowal_complete = "退会しました。";
//const m_select_action       = "あなたの行動を選択してください。";
//const m_recover_stamina     = "スタミナを回復しました。";
const m_battle_to             = "damage to the enemy.";
const m_battle_from           = "damage from the enemy.";
const m_battle_loose          = "You died.";
const m_battle_win            = "You win.";
const m_withdrowal_game       = "Delete data and cancel membership. This operation cannot be canceled. Are you sure?";
const m_withdrowal_complete   = "Your membership has been cancelled.";
const m_select_action         = "Command?";
const m_recover_stamina       = "Stamina has been regenerated.";
const m_purchase_gold         = "In-app purchase has been completed.";

function new_user() {
    let x = new XMLHttpRequest();
    let url = apiServer + apis.create;
    url = apiServer + "/create";
    x.open('POST', url);
    x.withCredentials = true;
    x.requestType = 'json';
    let data = { "user_name" : uid.text, "password" : passwd.text, "nick_name" : nickname.text };
    x.send(JSON.stringify(data));
    x.onreadystatechange = function(e) {
      if (this.readyState == 4 && this.status == 200) {
        let res = this.responseText;
        let json = JSON.parse(res);
        console.log(json);
        //if(json.result === "ok"){
            sessionStorage.setItem("new_user", res);
        //}
      }
    };
    1;
};

function login() {
    let x = new XMLHttpRequest();
    let url = apiServer + apis.login;
    url = apiServer + "/login";
    x.open('POST', url);
    x.withCredentials = true;
    x.requestType = 'json';
    let data = { "user_name" : uid.text, "password" : passwd.text };
    x.send(JSON.stringify(data));
    x.onreadystatechange = function(e) {
      if (this.readyState == 4 && this.status == 200) {
        let res = this.responseText;
        let json = JSON.parse(res);
        console.log(json);
        if(json.result === "ok"){
            //document.cookie = "session_id=" + json.session_id + "; SameSite=none";
            document.cookie = "session_id=" + json.session_id;
        }
        sessionStorage.setItem("login", JSON.stringify(json));
      }
    };
    1;
};

function user_id() {
    let x = new XMLHttpRequest();
    let url = apiServer + apis.user_id;
    url = apiServer + "/user_id";
    x.open('POST', url);
    x.withCredentials = true;
    x.requestType = 'json';
    x.send(null);
    x.onreadystatechange = function(e) {
      if (this.readyState == 4 && this.status == 200) {
        let res = this.responseText;
        let json = JSON.parse(res);
        console.log(json);
        if(json.result === "ok"){
            sessionStorage.setItem("pid", json.user_id);
        }
      }
    };
    1;
};

function delete_user() {
    sessionStorage.removeItem("delete_user");
    let deluser = () => {
        console.log("deluser");
        let x = new XMLHttpRequest();
        let url = apiServer + apis.delete;
        x.open('POST', url);
        x.withCredentials = true;
        x.requestType = 'json';
        x.send();
        x.onreadystatechange = function (e) {
            if (this.readyState == 4 && this.status == 200) {
                let res = this.responseText;
                let json = JSON.parse(res);
                console.log(json);
                if (json.result === "ok") {
                    console.log("delete: ok");
                }
                sessionStorage.setItem("delete_user", res);
                window.location = window.location;
            }
        };
    }
    //let ans = window.confirm("データを削除して退会します。本当によろしいですか？");
    let ans = window.confirm(m_withdrowal_game);
    if(ans){
	//setMessage(menu, "退会しました。");
        setMessage(menu, m_withdrowal_complete);
        setTimeout(deluser, 3000);
    }
    1;
};

function upload(fname="default.png", fdata="1") {
    sessionStorage.removeItem("upload");
    user_id();
    let senddata = () => {
        let ext = (fname.split("/").reverse()[0]).split('.').reverse()[0];
        let pid = sessionStorage.getItem('pid');
        let name = pid + "_" + Math.floor(Date.now() / 1000) + '.' + ext;
        let x = new XMLHttpRequest();
        let url = apiServer + apis.upload;
        x.open('POST', url);
        x.withCredentials = true;
        x.requestType = 'json';
        let data = { "file_name" : name, "file_data" : fdata };
        if (data.file_name !== "" && data.file_data !== "") {
            x.send(JSON.stringify(data));
            x.onreadystatechange = function (e) {
                if (this.readyState == 4 && this.status == 200) {
                    let res = this.responseText;
                    let json = JSON.parse(res);
                    console.log(json);
                    if (json.result === "ok") {
                        console.log("upload: ok");
                        player();
                    }
                    sessionStorage.setItem("upload", res);
                }
            };
        }
    };
    setTimeout(senddata, 1000);
    1;
};

function courseget() {
    let x = new XMLHttpRequest();
    let url = apiServer + apis.courseget;
    x.open('GET', url);
    x.withCredentials = true;
    x.requestType = 'json';
    x.send(null);
    x.onreadystatechange = function(e) {
      if (this.readyState == 4 && this.status == 200) {
        let res = this.responseText;
        let json = JSON.parse(res);
        console.log(json);
        if(json.result === "ok"){
            sessionStorage.setItem("courseget", res);
        }
      }
    };
    1;
};

function coursepost(id=1) {
    let x = new XMLHttpRequest();
    let url = apiServer + apis.coursepost;
    x.open('POST', url);
    x.withCredentials = true;
    x.requestType = 'json';
    let data = { "id" : id };
    x.send(JSON.stringify(data));
    x.onreadystatechange = function(e) {
      if (this.readyState == 4 && this.status == 200) {
        let res = this.responseText;
        let json = JSON.parse(res);
        console.log(json);
        if(json.result === "ok"){
            console.log("coursepost: ok");
        }
        sessionStorage.setItem("coursepost", res);
      }
    };
    1;
};

function action_attack() {
    let goToMenu = () => {
        actorSet.alpha = 0;
        actorAtk.alpha = 0;
        battleContainer = app.stage.removeChild(battleContainer);
        modeMenu();
        clearMessage(menu);
        //setMessage(menu, 'メニューから行動を選択してください。');
        setMessage(menu, m_select_action);
    };
    let x = new XMLHttpRequest();
    let url = apiServer + apis.battle;
    x.open('POST', url);
    x.withCredentials = true;
    x.requestType = 'json';
    let data = sessionStorage.getItem("coursepost");
    if (data === undefined || data === null ) {
        data = sessionStorage.getItem("battle");
        if(data === undefined || data === null ){
            return 1;
        }
    }
    console.log(data);
    sessionStorage.removeItem("coursepost");
    if ((JSON.parse(data)).result === "ok") {
        x.send(data);
        x.onreadystatechange = function (e) {
            if (this.readyState == 4 && this.status == 200) {
                let res = this.responseText;
                let json = JSON.parse(res);
                console.log(json);
                if (json.result === "ok") {
                    console.log("attack: ok");
                    if(json.phase === 2){
                        setMessage(battle, "");
                        let pl = () => {
                            //battleMessage1.text = "敵に" + json.player.str + "ダメージ与えた。"
                            battleMessage1.text = "" + json.player.str + " " + m_battle_to;
                        }
                        let en = () => {
                            //battleMessage2.text = "敵から" + json.enemy.str + "ダメージ受けた。"
                            battleMessage2.text = "" + json.enemy.str + " " + m_battle_from;
                        }
                        setTimeout(pl, 300);
                        setTimeout(en, 600);
                        let dmg = parseInt(sessionStorage.getItem("dmg"));
                        sessionStorage.setItem("dmg", (dmg + json.enemy.str));
                    }
                    else if(json.phase === 3){
                        if(json.status.result === "lose"){
                            let end = () => {
                                actorDead.alpha = 1;
                                actorAtk.alpha = 0;
                                //setMessage("battle", "敵に倒されてしまった・・・。");
                                setMessage("battle", m_battle_loose);
                                setTimeout(goToMenu, 1200);
                            };
                            setTimeout(end, 1200);
                        } else {
                            let end = () => {
                                sra1.alpha = 0;
                                sra2.alpha = 0;
                                sra3.alpha = 0;
                                sra4.alpha = 0;
                                sra5.alpha = 0;
                                //setMessage("battle", "敵を倒した。");
                                setMessage("battle", m_battle_win);
                                setTimeout(goToMenu, 1200);
                            };
                            setTimeout(end, 1200);
                        }
                        sessionStorage.setItem("dmg", 0);
                    }
                    setStat();
                }
                sessionStorage.setItem("battle", res);
            }
        };
    }
    1;
};

function player() {
    let x = new XMLHttpRequest();
    let url = apiServer + apis.player;
    x.open('GET', url);
    x.withCredentials = true;
    x.requestType = 'json';
    x.send(null);
    x.onreadystatechange = function(e) {
      if (this.readyState == 4 && this.status == 200) {
        let res = this.responseText;
        let json = JSON.parse(res);
        console.log(json);
        if(json.result === "ok"){
            sessionStorage.setItem("pinfo", res);
            pinfo = json;
        }
      }
    };
    1;
};

function action_charge() {
    let x = new XMLHttpRequest();
    let url = apiServer + apis.charge;
    x.open('POST', url);
    x.withCredentials = true;
    //x.requestType = 'json';
    x.setRequestHeader('Content-Type', 'application/json');
    let data = { "price" : price_charge };
    if (data.price > 0) {
        x.send(JSON.stringify(data));
        x.onreadystatechange = function (e) {
            if (this.readyState == 4 && this.status == 200) {
                let res = this.responseText;
                let json = JSON.parse(res);
                console.log(json);
                if (json.result === "ok") {
                    console.log("Charge: ok");
                }
                sessionStorage.setItem("charge", res);
            }
        };
    }
    1;
};

function action_stamina() {
    let x = new XMLHttpRequest();
    let url = apiServer + apis.recovery;
    x.open('POST', url);
    x.withCredentials = true;
    //x.requestType = 'json';
    x.setRequestHeader('Content-Type', 'application/json');
    let data = { "price" : price_stamina };
    if (data.price > 0) {
        x.send(JSON.stringify(data));
        x.onreadystatechange = function (e) {
            if (this.readyState == 4 && this.status == 200) {
                let res = this.responseText;
                let json = JSON.parse(res);
                console.log(json);
                if (json.result === "ok") {
                    console.log("Stamina recovery: ok");
                }
                sessionStorage.setItem("stamina", res);
            }
        };
    }
    1;
};

function action_gacha() {
    let x = new XMLHttpRequest();
    let url = apiServer + apis.gacha;
    x.open('POST', url);
    x.withCredentials = true;
    //x.requestType = 'json';
    x.setRequestHeader('Content-Type', 'application/json');
    let data = { "gold" : price_gacha };
    if (data.gold > 0) {
        x.send(JSON.stringify(data));
        x.onreadystatechange = function (e) {
            if (this.readyState == 4 && this.status == 200) {
                let res = this.responseText;
                let json = JSON.parse(res);
                console.log(json);
                if (json.result === "ok") {
                    console.log("Gacha: ok");
                }
                sessionStorage.setItem("gacha", res);
            }
        };
    }
    1;
};

function staminaCharge(e){
    console.log(e);
    action_stamina();
    let goToMenu = () => {
        staminaContainer = app.stage.removeChild(staminaContainer);
        modeMenu();
        clearMessage(menu);
        //setMessage(menu, 'メニューから行動を選択してください。');
        setMessage(menu, m_select_action);
    };

    clearMessage(stamina);
    //setMessage(stamina, 'スタミナを回復しました。');
    setMessage(stamina, m_recover_stamina);
    setTimeout(goToMenu, 800);
}

function goldCharge(e){
    console.log(e);
    action_charge();
    let goToMenu = () => {
        chargeContainer = app.stage.removeChild(chargeContainer);
        modeMenu();
        clearMessage(menu);
        //setMessage(menu, 'メニューから行動を選択してください。');
        setMessage(menu, m_select_action);
    };

    clearMessage(charge);
    //setMessage(charge, 'ゴールドを購入しました。');
    setMessage(charge, m_purchase_gold);
    setTimeout(goToMenu, 1800);
}

