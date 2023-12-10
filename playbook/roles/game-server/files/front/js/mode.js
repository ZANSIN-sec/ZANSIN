//const m_mode_select   = 'コマンドを選択してください';
//const m_mode_battle1  = " 名前: ";
//const m_mode_battle2  = ", 消費スタミナ: ";
//const m_mode_purchase = '課金してゴールドを購入しますか？');
//const m_mode_stamina  = 'ゴールドを消費してスタミナを回復しますか？');
//const m_mode_gacha    = 'ここはガチャの店だ。　　　　　　　　金は払ってもらうが、ガチャをまわせば武器や防具を強化できかもしれないぞ。');

const m_mode_select    = 'Command?';
const m_mode_battle1   = " Name: ";
const m_mode_battle2   = ", Stamina: ";
const m_mode_purchase  = 'Would you like to pay to purchase   GOLD?';
const m_mode_stamina   = 'Would you like to spend gold to     restore stamina?';
const m_mode_gacha     = 'Hello, this is Gacha Machine, you   can get weapons and armor by        spending 100 GOLD. You may get SUPER RARE ITEMS!';

function jumpModeMenu() {
    clearInterval(openingTimer);
    modeMenu();
}

function modeMenu(){
    player();
    sessionStorage.setItem("dmg", 0);
    openingContainer = app.stage.removeChild(openingContainer);
    menuContainer.alpha = 1;
    setActorWlkStatusMode();
    actorWlk.play();
    app.stage.addChild(menuContainer);
    //setMessage(menu, 'コマンドを選択してください');
    setMessage(menu, m_mode_select); 
    setTimeout(setStat, 1000);
    cmdMenuInteractiveOn();
}

function modeCourse(){
    player();
    courseget();

    let makeCourseMesage = (c) => {
        return m_mode_battle1 + c.name + m_mode_battle2 + c.stamina;
    };

    let goToCourse = () => {
        if(sessionStorage.getItem('courseget') !== null && (JSON.parse(sessionStorage.getItem('courseget'))).result === "ok") {
          let course = (JSON.parse(sessionStorage.getItem('courseget'))).course;
          cmdCourseTxt2.text  = makeCourseMesage(course[0]);
          cmdCourseTxt4.text  = makeCourseMesage(course[1]);
          cmdCourseTxt6.text  = makeCourseMesage(course[2]);
          cmdCourseTxt8.text  = makeCourseMesage(course[3]);
          cmdCourseTxt10.text = makeCourseMesage(course[4]);
          courseContainer.alpha = 1;
          menuCommandContainer = app.stage.removeChild(menuCommandContainer);
          app.stage.addChild(courseContainer);
        }
    };

    setTimeout(goToCourse, 1000);
    setTimeout(setStat, 1000);
}

function modeBattle(){
    player();
    battleContainer.alpha = 1;
    actorDead.alpha = 0;
    setActorWlkBattleMode();
    menuCommandContainer = app.stage.removeChild(menuCommandContainer);
    cmdMenuInteractiveOff();
    app.stage.addChild(battleContainer);
    //setMessage(battle, 'コマンドを選択してください');
    setMessage(battle, m_mode_select);
    setTimeout(setStat, 1000);
}

function modeStatus(){
    pstatContainer.alpha = 1;
    actorWlk.alpha - 0;
    menuCommandContainer = app.stage.removeChild(menuCommandContainer);
    cmdMenuInteractiveOff();
    app.stage.addChild(pstatContainer);
    let loadTexture;

    player();
    
    let disp = () => {
        let data = sessionStorage.getItem("pinfo");
        if(data !== undefined && (JSON.parse(data)).result === "ok"){
           pinfo = JSON.parse(data);
            console.log(data);
            let stat = {
                /*
		"名前" : pinfo.nick_name,
                "レベル" : pinfo.level,
                "体力" : pinfo.max_hp,
                "攻撃力" : pinfo.max_str,
                "武器" : pinfo.weapon_name,
                "武器の攻撃力" : pinfo.weapon_param,
                "防具" : pinfo.armor_name,
                "防具の防御力" : pinfo.armor_param,
                "スタミナ" : pinfo.stamina,
                "最大スタミナ" : pinfo.max_stamina,
                "ゴールド" : pinfo.gold,
                "経験値" : pinfo.exp,
                "次のレベルまで" : pinfo.need_exp
                */
		"Name" : pinfo.nick_name,
                "Level" : pinfo.level,
                "HP" : pinfo.max_hp,
                "STR" : pinfo.max_str,
                "Weapon" : pinfo.weapon_name,
                "WeaponSpec" : pinfo.weapon_param,
                "Armor" : pinfo.armor_name,
                "ArmorSpec" : pinfo.armor_param,
                "Stamina" : pinfo.stamina,
                "MaxStamina" : pinfo.max_stamina,
                "GOLD" : pinfo.gold,
                "Exp" : pinfo.exp,
                "NextLevel" : pinfo.need_exp
            };
            //let arr = ["名前", "レベル", "体力", "攻撃力", "武器", "武器の攻撃力", "防具", "防具の防御力", "スタミナ", "最大スタミナ", "ゴールド", "経験値", "次のレベルまで" ];
            let arr = ["Name", "Level", "HP", "STR", "Weapon", "WeaponSpec", "Armor", "ArmorSpec", "Stamina", "MaxStamina", "GOLD", "Exp", "NextLevel" ];
            clearMessage(pstat);
            for(let i = 0; i < arr.length; i++){
                let elm = 'pstatMessage' + String(i+1);
                window[elm].text = arr[i] + ": " + stat[arr[i]];
            }
        } else {
            console.log("ERROR: pinfo get error");
        }

    };
    let imgview = () => {
        myimage = new PIXI.Sprite(loadTexture);
        myimage.anchor.set(0.5);
        if(myimage.width > 72 || myimage.height > 72){
            let x = Math.floor((myimage.width / 72));
            let y = Math.floor((myimage.height / 72));
            let xx = x;
            if(y > x){
                xx = y;
            }
            myimage.scale.x = (1 / xx);
            myimage.scale.y = (1 / xx);
        } else {
            myimage.scale.x = 1;
            myimage.scale.y = 1;
        }
        myimage.x = app.stage.width  / 16 * 13 - 0;
        myimage.y = app.stage.height / 8 * 7 + 0;
        myimage.interactive = true;
        myimage.buttonMode = true;
        myimage.on('pointertap', uploadFile);
        pstatContainer.addChild(myimage);
    }
    let getMyimage = () => {
        pstatContainer.removeChild(myimage);
        let image = (JSON.parse(sessionStorage.getItem('pinfo'))).image;
        if(image !== "default.png"){
            //let oldMyimage = pstatContainer.removeChild(myimage);
            loadTexture = new PIXI.Texture.from(apiServer + '/images/players/' + image);

        }
        pstatContainer.removeChild(myimageButton);
        pstatContainer.addChild(myimageButton);
        setTimeout(imgview, 1000);
    }
    setTimeout(disp, 2000);
    setTimeout(setStat, 1000);
    setTimeout(getMyimage, 1000);
}

function modeStamina(){
    player();
    staminaContainer.alpha = 1;
    actorWlk.alpha = 0;
    menuCommandContainer = app.stage.removeChild(menuCommandContainer);
    cmdMenuInteractiveOff();
    app.stage.addChild(staminaContainer);
    //setMessage(stamina, 'ゴールドを消費してスタミナを回復しますか？');
    setMessage(stamina, m_mode_stamina);
    setTimeout(setStat, 1000);
}

function modeGatya(){
    player();
    gachaContainer.alpha = 1;
    actorWlk.alpha = 0;
    menuCommandContainer = app.stage.removeChild(menuCommandContainer);
    cmdMenuInteractiveOff();
    setCapsuleDefault();
    app.stage.addChild(gachaContainer);
    //setMessage(gacha, 'ここはガチャの店だ。　　　　　　　　金は払ってもらうが、ガチャをまわせば武器や防具を強化できかもしれないぞ。');
    setMessage(gacha, m_mode_gacha);
    setTimeout(setStat, 1000);
}

function modeCharge(){
    player();
    gachaContainer.alpha = 1;
    actorWlk.alpha = 0;
    menuCommandContainer = app.stage.removeChild(menuCommandContainer);
    cmdMenuInteractiveOff();
    app.stage.addChild(chargeContainer);
    //setMessage(charge, '課金してゴールドを購入しますか？');
    setMessage(charge, m_mode_purchase);
    setTimeout(setStat, 1000);
}
