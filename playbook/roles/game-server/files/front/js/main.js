//const pixiSound = require('pixi-sound');
let price_charge  = 1000;
let price_stamina = 100;
let price_gacha   = 100;

//var apiServer = "http://192.168.159.128";
var apiServer = location.origin;

let apis = {
    create : "/create",
    login : "/login",
    user_id : "/user_id",
    upload : "/upload",
    delete : "/delete_user",
    courseget : "/courseget",
    coursepost : "/coursepost",
    battle : "/battle",
    recovery : "/recovery",
    gacha : "/gacha",
    player : "/player",
    charge : "/charge"
};

let account = {
    "user" : "foo",
    "pass" : "bar"
};

// for multibyte character set
PIXI.TextMetrics.BASELINE_SYMBOL = "あ｜";

//
// event listener
//
document.getElementById('file').addEventListener('change', evnt => {
    // read file
    let files = evnt.target.files;
    if (!files.length) {
        console.log('error! file are not uploaded.');
        return;
    }
    // read upload image
    let image = new Image();
    let fr = new FileReader();
    fr.readAsDataURL(files[0]);

    // register eventlistener
    fr.onload = evnt => {
        // convert to base64
        let b64data = evnt.target.result.split(',').reverse()[0];
        upload(files[0].name, b64data);
        // set base64 url
        image.src = evnt.target.result;
        // set eventlistener
        image.onload = () => {
            let oldMyimage = pstatContainer.removeChild(myimage);
            // display upload image
            let loadTexture = new PIXI.Texture(new PIXI.BaseTexture(image));
            myimage = new PIXI.Sprite(loadTexture);
            console.log(myimage.width);
            myimage.anchor.set(0.5);
            if(myimage.width > 72){
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
        };
    }
});

var openingTimer;

// create Pixi App
let app = new PIXI.Application({
    width: 600,                 // screen view
    height: 600,                // screen view
    backgroundColor: 0x1099bb,  // bg-color
    autoDensity: true,
});
// create canvas
let el = document.getElementById('app');
el.appendChild(app.view);



// title sound
//pixiSound.add('title', './sound/8bit-Prologue01.mp3');

const battle = 'battle';
const gacha = 'gacha';
const pstat = 'pstat';
const stamina = 'stamina';
const charge = 'charge';
const menu = 'menu';

// sample data
let pinfo = {"armor_id":23,"armor_name":"Bulletproof Vest","armor_param":21,"armor_rarity":"N","created_at":"2021-01-24T07:18:01","exp":3,"gold":682,"id":12,"image":"a","level":1,"max_hp":15,"max_stamina":10,"max_str":5,"need_exp":2,"nick_name":"mahoyaya","password":"password","result":"ok","stamina":10,"staminaupdated_at":"2021-01-24T07:22:07","user_name":"mahoyaya","weapon_id":10,"weapon_name":"Steel Broadsword","weapon_param":30,"weapon_rarity":"R"};
let pid = "";

/** =======================================================================================
 *
 */

// create new container
let openingContainer = new PIXI.Container();
openingContainer.x = 0;
openingContainer.y = 0;
openingContainer.zIndex = 100;
app.stage.addChild(openingContainer);

// set bg-color and screen size
let bgSprite = new PIXI.Sprite(PIXI.Texture.WHITE);
//bgSprite.anchor.set(0.5);
bgSprite.width = app.screen.width;
bgSprite.height = app.screen.height;
bgSprite.tint = 0x333366;
openingContainer.addChild(bgSprite);



let uid = new PIXI.TextInput({
    input: {
        fontFamily: 'Arial',
        fontSize: '20px',
        padding: '12px',
        width: '300px',
        color: '#26272E'
    },
    box: {
        default: {fill: 0xE8E9F3, rounded: 12, stroke: {color: 0xCBCEE0, width: 3}},
        focused: {fill: 0xE1E3EE, rounded: 12, stroke: {color: 0xABAFC6, width: 3}},
        disabled: {fill: 0xDBDBDB, rounded: 12}
    }
})

uid.placeholder = 'Enter your User ID';
uid.x = app.stage.width / 2;
uid.y = app.stage.height / 2 - 64;
uid.pivot.x = uid.width / 2;
uid.pivot.y = uid.height / 2;
openingContainer.addChild(uid);

let passwd = new PIXI.TextInput({
    input: {
        fontFamily: 'Arial',
        fontSize: '20px',
        padding: '12px',
        width: '300px',
        color: '#26272E'
    },
    box: {
        default: {fill: 0xE8E9F3, rounded: 12, stroke: {color: 0xCBCEE0, width: 3}},
        focused: {fill: 0xE1E3EE, rounded: 12, stroke: {color: 0xABAFC6, width: 3}},
        disabled: {fill: 0xDBDBDB, rounded: 12}
    }
})

passwd.placeholder = 'Enter your Password';
passwd.x = app.stage.width / 2;
passwd.y = app.stage.height / 2;
passwd.pivot.x = passwd.width / 2;
passwd.pivot.y = passwd.height / 2;
openingContainer.addChild(passwd);

let nickname = new PIXI.TextInput({
    input: {
        fontFamily: 'Arial',
        fontSize: '20px',
        padding: '12px',
        width: '300px',
        color: '#26272E'
    },
    box: {
        default: {fill: 0xE8E9F3, rounded: 12, stroke: {color: 0xCBCEE0, width: 3}},
        focused: {fill: 0xE1E3EE, rounded: 12, stroke: {color: 0xABAFC6, width: 3}},
        disabled: {fill: 0xDBDBDB, rounded: 12}
    }
})

nickname.placeholder = 'Enter your nickname';
nickname.x = app.stage.width / 2;
nickname.y = app.stage.height / 2 + 64;
nickname.pivot.x = nickname.width / 2;
nickname.pivot.y = nickname.height / 2;
openingContainer.addChild(nickname);
nickname.alpha = 0;


/* end opening */


function createSelectContainer() {
    // create container
    let selectContainer = new PIXI.Container();

    selectContainer.x = app.screen.width * 0.1;
    selectContainer.y = app.screen.height * 0.1;

    //  set new objects
   let selectbox = new PIXI.Graphics()
    .beginFill(0x000000)
    .drawRect(0,0,app.screen.width * 0.8,app.screen.height * 0.8)
    .endFill();


    // frame
    let selectframe = new PIXI.Graphics()
    .lineStyle(8, 0xffffff)     // line style
    .drawRect(0,0,app.screen.width * 0.8,app.screen.height * 0.8)  
    .endFill();
    selectframe.x = 0;
    selectframe.y = 0;
    selectContainer.addChild(selectframe);

    // set to container
    selectContainer.addChild(selectbox);

    return selectContainer;
}


function createCommandContainer() {
    let commandContainer = new PIXI.Container();

    commandContainer.x = app.screen.width * 0.05;
    commandContainer.y = app.screen.height - 220;

    let commandbox = new PIXI.Graphics()
    .beginFill(0x000000)
    .drawRect(0,0,app.screen.width * 0.2,app.screen.height * 0.3)
    .endFill();


    let commandframe = new PIXI.Graphics()
    .lineStyle(8, 0xffffff)
    .drawRect(0,0,app.screen.width * 0.2,app.screen.height * 0.3)  
    .endFill();
    commandframe.x = 0;
    commandframe.y = 0;
    commandContainer.addChild(commandframe);

    commandContainer.addChild(commandbox);

    return commandContainer;
}

function createMessageContainer() {
    let messageContainer = new PIXI.Container();

    messageContainer.x = app.screen.width * 0.3;
    messageContainer.y = app.screen.height - 220;

    let messagebox = new PIXI.Graphics()
    .beginFill(0x000000)
    .drawRect(0,0,app.screen.width * 0.65,app.screen.height * 0.3)
    .endFill();


    let messageframe = new PIXI.Graphics()
    .lineStyle(8, 0xffffff)
    .drawRect(0,0,app.screen.width * 0.65,app.screen.height * 0.3)  
    .endFill();
    messageframe.x = 0;
    messageframe.y = 0;
    messageContainer.addChild(messageframe);

    messageContainer.addChild(messagebox);

    return messageContainer;
}


function createPstatContainer() {
    let pstatContainer = new PIXI.Container();

    pstatContainer.x = app.screen.width * 0.3;
    pstatContainer.y = app.screen.height * 0.05;

    let pstatBox = new PIXI.Graphics()
    .beginFill(0x000000)
    .drawRect(0,0,app.screen.width * 0.65,app.screen.height * 0.88)
    .endFill();


    let pstatFrame = new PIXI.Graphics()
    .lineStyle(8, 0xffffff)
    .drawRect(0,0,app.screen.width * 0.65,app.screen.height * 0.88)  
    .endFill();
    pstatFrame.x = 0;
    pstatFrame.y = 0;
    pstatContainer.addChild(pstatFrame);

    pstatContainer.addChild(pstatBox);

    return pstatContainer;
}


/** =======================================================================================
 * 
 */

let statusContainer = new PIXI.Container();

statusContainer.x = app.screen.width * 0.05;
statusContainer.y = app.screen.height * 0.05;

let statusbox = new PIXI.Graphics()
.beginFill(0x000000)
.drawRect(0,0,app.screen.width * 0.2,app.screen.height * 0.3)
.endFill();


let statusframe = new PIXI.Graphics()
.lineStyle(8, 0xffffff)
.drawRect(0,0,app.screen.width * 0.2,app.screen.height * 0.3)  
.endFill();
statusframe.x = 0;
statusframe.y = 0;
statusContainer.addChild(statusframe);

statusContainer.addChild(statusbox);
statusContainer.alpha = 1;
app.stage.addChild(statusContainer);



/** =======================================================================================
 * 
 */

let commandContainer = new PIXI.Container();

commandContainer.x = app.screen.width * 0.05;
commandContainer.y = app.screen.height - 220;

let commandbox = new PIXI.Graphics()
.beginFill(0x000000)
.drawRect(0,0,app.screen.width * 0.2,app.screen.height * 0.3)
.endFill();


let commandframe = new PIXI.Graphics()
.lineStyle(8, 0xffffff)
.drawRect(0,0,app.screen.width * 0.2,app.screen.height * 0.3)  
.endFill();
commandframe.x = 0;
commandframe.y = 0;
commandContainer.addChild(commandframe);

commandContainer.addChild(commandbox);




/** =======================================================================================
 * 
 */

let messageContainer = new PIXI.Container();

messageContainer.x = app.screen.width * 0.3;
messageContainer.y = app.screen.height - 220;

let messagebox = new PIXI.Graphics()
.beginFill(0x000000)
.drawRect(0,0,app.screen.width * 0.65,app.screen.height * 0.3)
.endFill();


let messageframe = new PIXI.Graphics()
.lineStyle(8, 0xffffff)
.drawRect(0,0,app.screen.width * 0.65,app.screen.height * 0.3)  
.endFill();
messageframe.x = 0;
messageframe.y = 0;
messageContainer.addChild(messageframe);

messageContainer.addChild(messagebox);





// start menu
let menuContainer = new PIXI.Container();
let menuCommandContainer = createCommandContainer();
let menuMessageContainer = createMessageContainer();
menuContainer.addChild(menuMessageContainer);
menuContainer.addChild(menuCommandContainer);

// course select
let courseSelectContainer = createSelectContainer();
let courseContainer = new PIXI.Container();
courseContainer.addChild(courseSelectContainer);

// battle
let battleCommandContainer = createCommandContainer();
let battleMessageContainer = createMessageContainer();
let battleContainer = new PIXI.Container();
battleContainer.addChild(battleCommandContainer);
battleContainer.addChild(battleMessageContainer);

// gacha
let gachaCommandContainer = createCommandContainer();
let gachaMessageContainer = createMessageContainer();
let gachaContainer = new PIXI.Container();
gachaContainer.addChild(gachaMessageContainer);
gachaContainer.addChild(gachaCommandContainer);

// status
let pstatCommandContainer = createCommandContainer();
let pstatMessageContainer = createPstatContainer(); 
let pstatContainer = new PIXI.Container();
pstatContainer.addChild(pstatMessageContainer);
pstatContainer.addChild(pstatCommandContainer);




// stamina
let staminaCommandContainer = createCommandContainer();
let staminaMessageContainer = createMessageContainer();
let staminaContainer = new PIXI.Container();
staminaContainer.addChild(staminaMessageContainer);
staminaContainer.addChild(staminaCommandContainer);



// charge
let chargeCommandContainer = createCommandContainer();
let chargeMessageContainer = createMessageContainer();
let chargeContainer = new PIXI.Container();
chargeContainer.addChild(chargeMessageContainer);
chargeContainer.addChild(chargeCommandContainer);



//const m_main_login = 'ゲームにログインしてください';
const m_main_login = 'Login';



/*
* web font setting
*/
WebFont.load (
    {
        custom:
        {
            families: ['PixelMplus10', 'PixelMplus12'],
            urls: ['./css/font.css']
        },
        active: () =>
        {
            /*
            * opening
            */
            //loginTxt =  createMessage('ゲームにログインしてください',app.screen.width / 2,app.screen.height / 3 - 64); 
            loginTxt =  createMessage(m_main_login, app.screen.width / 2,app.screen.height / 3 - 64); 
            loginTxt.name = 'labelLogin';
            loginTxt.anchor.set(0.5);
            openingContainer.addChild(loginTxt);

            login2Txt = createMessage('',app.screen.width / 2,app.screen.height / 3 - 32);
            login2Txt.name = 'labelError';
            login2Txt.alpha = 1;
            login2Txt.anchor.set(0.5);
            openingContainer.addChild(login2Txt);

            startTxt = createIntMessage('empty',app.screen.width / 2, app.screen.height / 2);
            startTxt.name = 'clickToStart';
            startTxt.alpha = 0;
            startTxt.anchor.set(0.5);
            startTxt.interactive = false;
            openingContainer.addChild(startTxt);

            copyrightTxt = createIntMessage('🄫 MINI Hardening',app.screen.width / 2, app.screen.height / 10 * 9);
            copyrightTxt.name = 'copyright';
            copyrightTxt.alpha = 0;
            copyrightTxt.anchor.set(0.5);
            openingContainer.addChild(copyrightTxt);

            /*
            * status menu
            */
            statTxt1 = createIntMessage(' ', 8, 6);
            statusContainer.addChild(statTxt1);

            statTxt2 = createIntMessage('H: ', 8, 36);
            statusContainer.addChild(statTxt2);

            statTxt3 = createIntMessage('A: ', 8, 66);
            statusContainer.addChild(statTxt3);

            statTxt4 = createIntMessage('L: ', 8, 96);
            statusContainer.addChild(statTxt4);

            statTxt5 = createIntMessage('S: ', 8, 126);
            statusContainer.addChild(statTxt5);

            statTxt6 = createIntMessage('G: ', 8, 156);
            statusContainer.addChild(statTxt6);



            /*
             * various window messages
             */
            battleMessage1 =  createMessage('Sample Message line1',8,8); 
            battleMessageContainer.addChild(battleMessage1);
            
            battleMessage2 =  createMessage('line2',8,40); 
            battleMessageContainer.addChild(battleMessage2);
            
            battleMessage3 =  createMessage('line3',8,72); 
            battleMessageContainer.addChild(battleMessage3);
            
            battleMessage4 =  createMessage('line4',8,104); 
            battleMessageContainer.addChild(battleMessage4);
            
            battleMessage5 =  createMessage('line5',8,136); 
            battleMessageContainer.addChild(battleMessage5);
            
            menuMessage1 =  createMessage('Sample Message line1',8,8); 
            menuMessageContainer.addChild(menuMessage1);
            
            menuMessage2 =  createMessage('line2',8,40); 
            menuMessageContainer.addChild(menuMessage2);
            
            menuMessage3 =  createMessage('line3',8,72); 
            menuMessageContainer.addChild(menuMessage3);
            
            menuMessage4 =  createMessage('line4',8,104); 
            menuMessageContainer.addChild(menuMessage4);
            
            menuMessage5 =  createMessage('line5',8,136); 
            menuMessageContainer.addChild(menuMessage5);
            
            gachaMessage1 =  createMessage('Sample Message line1',8,8); 
            gachaMessageContainer.addChild(gachaMessage1);
            
            gachaMessage2 =  createMessage('line2',8,40); 
            gachaMessageContainer.addChild(gachaMessage2);
            
            gachaMessage3 =  createMessage('line3',8,72); 
            gachaMessageContainer.addChild(gachaMessage3);
            
            gachaMessage4 =  createMessage('line4',8,104); 
            gachaMessageContainer.addChild(gachaMessage4);
            
            gachaMessage5 =  createMessage('line5',8,136); 
            gachaMessageContainer.addChild(gachaMessage5);
            
            staminaMessage1 =  createMessage('Sample Message line1',8,8); 
            staminaMessageContainer.addChild(staminaMessage1);
            
            staminaMessage2 =  createMessage('line2',8,40); 
            staminaMessageContainer.addChild(staminaMessage2);
            
            staminaMessage3 =  createMessage('line3',8,72); 
            staminaMessageContainer.addChild(staminaMessage3);
            
            staminaMessage4 =  createMessage('line4',8,104); 
            staminaMessageContainer.addChild(staminaMessage4);
            
            staminaMessage5 =  createMessage('line5',8,136); 
            staminaMessageContainer.addChild(staminaMessage5);
            
            chargeMessage1 =  createMessage('Sample Message line1',8,8); 
            chargeMessageContainer.addChild(chargeMessage1);
            
            chargeMessage2 =  createMessage('line2',8,40); 
            chargeMessageContainer.addChild(chargeMessage2);
            
            chargeMessage3 =  createMessage('line3',8,72); 
            chargeMessageContainer.addChild(chargeMessage3);
            
            chargeMessage4 =  createMessage('line4',8,104); 
            chargeMessageContainer.addChild(chargeMessage4);
            
            chargeMessage5 =  createMessage('line5',8,136); 
            chargeMessageContainer.addChild(chargeMessage5);



        },
        inactive: () =>
        {
            // can't load web fonts
            console.log('font loading failed');
        }
    });

////// create text data //////

/*
* menu command
*/
const m_main_battle   = 'BATTLE';
const m_main_status   = 'STATUS';
const m_main_inn      = 'INN';
const m_main_gacha    = 'GACHA';
const m_main_store    = 'STORE';
//const m_main_attack = 'たたかう';
//const m_main_defend = 'ぼうぎょ';
//const m_main_spells = 'まほう'; 
//const m_main_run   = 'にげる'; 
const m_main_attack  = 'Attack';
const m_main_defend  = 'Defend';
const m_main_spells  = 'Spells'; 
const m_main_run     = 'Run'; 
//const m_main_pull = 'ガチャひく';
//const m_main_back = 'もどる';
const m_main_pull = 'PULL';
const m_main_back = 'BACK';
//const m_main_regen = '回復する';
const m_main_regen = 'REGENERATE';
//const m_main_purchase = '課金する';
const m_main_purchase = 'PURCHASE';
//let arr = ["名前", "レベル", "体力", "攻撃力", "武器", "武器の攻撃力", "防具", "防具の防御力", "スタミナ", "最大スタミナ", "ゴールド", "経験値", "次のレベルまで" ];
let arr = ["Name", "Level", "HP", "STR", "Weapon", "WeaponSpec", "Armor", "ArmorSpec", "Stamina", "MaxStamina", "GOLD", "Exp", "NextLevel" ];
const m_main_name       = 'Name';
const m_main_level      = 'Level';
const m_main_hp         = 'HP';
const m_main_str        = 'STR';
const m_main_weapon     = 'Weapon';
const m_main_weaponspec = 'WeaponSpec';
const m_main_armor      = 'Armor';
const m_main_armorspec  = 'ArmorSpec';
const m_main_stamina    = 'Stamina';
const m_main_maxstamina = 'MaxStamina';
const m_main_gold       = 'GOLD';
const m_main_exp        = 'Exp';
const m_main_nextlevel  = 'NextLevel';
//const m_main_course01 = '★コース１';
//const m_main_course02 = ' コース１の説明';
//const m_main_course03 = '★コース２';
//const m_main_course04 = ' コース２の説明';
//const m_main_course05 = '★コース３';
//const m_main_course06 = ' コース３の説明';
//const m_main_course07 = '★コース４';
//const m_main_course08 = ' コース４の説明';
//const m_main_course09 = '★コース５';
//const m_main_course10 = ' コース５の説明';
//const m_main_course11 = '        ';
//const m_main_course12 = 'もどる';
//const m_main_course13 = '        ';
//const m_main_course14 = '        ';
//const m_main_course15 = '        ';
const m_main_course01 = 'Course 1';
const m_main_course02 = ' Description: ';
const m_main_course03 = 'Course 2';
const m_main_course04 = ' Description: ';
const m_main_course05 = 'Course 3';
const m_main_course06 = ' Description: ';
const m_main_course07 = 'Course 4';
const m_main_course08 = ' Description: ';
const m_main_course09 = 'Course 5';
const m_main_course10 = ' Description: ';
const m_main_course11 = '        ';
const m_main_course12 = 'Back to menu';
const m_main_course13 = '        ';
const m_main_course14 = '        ';
const m_main_course15 = '        ';

const cmdMenuTxt1 = createIntMessage(m_main_battle, 8, 8);
cmdMenuTxt1.on('pointertap',modeCourse);
cmdMenuTxt1.interactive = false;
menuCommandContainer.addChild(cmdMenuTxt1);

const cmdMenuTxt2 = createIntMessage(m_main_status, 8, 40);
cmdMenuTxt2.on('pointertap',modeStatus);
cmdMenuTxt2.interactive = false;
menuCommandContainer.addChild(cmdMenuTxt2);

const cmdMenuTxt3 = createIntMessage(m_main_inn, 8, 72);
cmdMenuTxt3.on('pointertap',modeStamina);
cmdMenuTxt3.interactive = false;
menuCommandContainer.addChild(cmdMenuTxt3);

const cmdMenuTxt4 = createIntMessage(m_main_gacha, 8, 104);
cmdMenuTxt4.on('pointertap',modeGatya);
cmdMenuTxt4.interactive = false;
menuCommandContainer.addChild(cmdMenuTxt4);

const cmdMenuTxt5 = createIntMessage(m_main_store, 8, 136);
cmdMenuTxt5.on('pointertap',modeCharge);
cmdMenuTxt5.interactive = false;
menuCommandContainer.addChild(cmdMenuTxt5);

/*
* battle menu
*/
const cmdTxt1 = createIntMessage(m_main_attack, 8, 8);
cmdTxt1.on('pointertap',doBattle);
battleCommandContainer.addChild(cmdTxt1);

const cmdTxt2 = createIntMessage(m_main_defend, 8, 40);
cmdTxt2.on('pointertap',doGuard);
battleCommandContainer.addChild(cmdTxt2);

const cmdTxt3 = createIntMessage(m_main_spells, 8, 72);
cmdTxt3.on('pointertap',doMagic);
battleCommandContainer.addChild(cmdTxt3);

const cmdTxt4 = createIntMessage(m_main_run, 8, 104);
cmdTxt4.on('pointertap',doEscape);
battleCommandContainer.addChild(cmdTxt4);

/*
 * player status window
 */
pstatMessage1 =  createMessage(m_main_name,8,8); 
pstatMessageContainer.addChild(pstatMessage1);

pstatMessage2 =  createMessage(m_main_level,8,40); 
pstatMessageContainer.addChild(pstatMessage2);

pstatMessage3 =  createMessage(m_main_hp,8,72); 
pstatMessageContainer.addChild(pstatMessage3);

pstatMessage4 =  createMessage(m_main_str,8,104); 
pstatMessageContainer.addChild(pstatMessage4);

pstatMessage5 =  createMessage(m_main_weapon,8,136); 
pstatMessageContainer.addChild(pstatMessage5);

pstatMessage6 =  createMessage(m_main_weaponspec,8,168); 
pstatMessageContainer.addChild(pstatMessage6);

pstatMessage7 =  createMessage(m_main_armor,8,200); 
pstatMessageContainer.addChild(pstatMessage7);

pstatMessage8 =  createMessage(m_main_armorspec,8,232); 
pstatMessageContainer.addChild(pstatMessage8);

pstatMessage9 =  createMessage(m_main_stamina,8,264); 
pstatMessageContainer.addChild(pstatMessage9);

pstatMessage10 =  createMessage(m_main_maxstamina,8,296); 
pstatMessageContainer.addChild(pstatMessage10);

pstatMessage11 =  createMessage(m_main_gold,8,328); 
pstatMessageContainer.addChild(pstatMessage11);

pstatMessage12 =  createMessage(m_main_exp,8,360); 
pstatMessageContainer.addChild(pstatMessage12);

pstatMessage13 =  createMessage(m_main_nextlevel,8,392); 
pstatMessageContainer.addChild(pstatMessage13);

pstatMessage14 =  createMessage(' ',8,424); 
pstatMessageContainer.addChild(pstatMessage14);

pstatMessage15 =  createMessage(' ',8,456); 
pstatMessageContainer.addChild(pstatMessage15);


/*
*  gacha menu
*/
const cmdGatyaTxt1 = createIntMessage(m_main_pull, 8, 8);
cmdGatyaTxt1.on('pointertap',gachaFetch);
gachaCommandContainer.addChild(cmdGatyaTxt1);

const cmdGatyaTxt2 = createIntMessage(m_main_back, 8, 40);
cmdGatyaTxt2.on('pointertap',doGatyaToMenu);
gachaCommandContainer.addChild(cmdGatyaTxt2);

/*
* stamina menu
*/
const cmdStaminaTxt1 = createIntMessage(m_main_regen, 8, 8);
cmdStaminaTxt1.on('pointertap',staminaCharge);
staminaCommandContainer.addChild(cmdStaminaTxt1);

const cmdStaminaTxt2 = createIntMessage(m_main_back, 8, 40);
cmdStaminaTxt2.on('pointertap',doStaminaToMenu);
staminaCommandContainer.addChild(cmdStaminaTxt2);

/*
* status menu
*/
const cmdPstatTxt1 = createIntMessage(m_main_back, 8, 8);
cmdPstatTxt1.on('pointertap',doPstatToMenu);
pstatCommandContainer.addChild(cmdPstatTxt1);

/*
* charge menu
*/
const cmdChargeTxt1 = createIntMessage(m_main_purchase, 8, 8);
cmdChargeTxt1.on('pointertap',goldCharge);
chargeCommandContainer.addChild(cmdChargeTxt1);

const cmdChargeTxt2 = createIntMessage(m_main_back, 8, 40);
cmdChargeTxt2.on('pointertap',doChargeToMenu);
chargeCommandContainer.addChild(cmdChargeTxt2);

/*
* course select window
*/
const cmdCourseTxt1 = createIntMessage(m_main_course01, 8, 8);
cmdCourseTxt1.on('pointertap',courseToBattle1);
courseSelectContainer.addChild(cmdCourseTxt1);

const cmdCourseTxt2 = createIntMessage(m_main_course02, 8, 40);
cmdCourseTxt2.on('pointertap',courseToBattle1);
courseSelectContainer.addChild(cmdCourseTxt2);

const cmdCourseTxt3 = createIntMessage(m_main_course03, 8, 72);
cmdCourseTxt3.on('pointertap',courseToBattle2);
courseSelectContainer.addChild(cmdCourseTxt3);

const cmdCourseTxt4 = createIntMessage(m_main_course04, 8, 104);
cmdCourseTxt4.on('pointertap',courseToBattle2);
courseSelectContainer.addChild(cmdCourseTxt4);

const cmdCourseTxt5 = createIntMessage(m_main_course05, 8, 136);
cmdCourseTxt5.on('pointertap',courseToBattle3);
courseSelectContainer.addChild(cmdCourseTxt5);

const cmdCourseTxt6 = createIntMessage(m_main_course06, 8, 168);
cmdCourseTxt6.on('pointertap',courseToBattle3);
courseSelectContainer.addChild(cmdCourseTxt6);

const cmdCourseTxt7 = createIntMessage(m_main_course07, 8, 200);
cmdCourseTxt7.on('pointertap',courseToBattle4);
courseSelectContainer.addChild(cmdCourseTxt7);

const cmdCourseTxt8 = createIntMessage(m_main_course08, 8, 232);
cmdCourseTxt8.on('pointertap',courseToBattle4);
courseSelectContainer.addChild(cmdCourseTxt8);

const cmdCourseTxt9 = createIntMessage(m_main_course09, 8, 264);
cmdCourseTxt9.on('pointertap',courseToBattle5);
courseSelectContainer.addChild(cmdCourseTxt9);

const cmdCourseTxt10 = createIntMessage(m_main_course10, 8, 296);
cmdCourseTxt10.on('pointertap',courseToBattle5);
courseSelectContainer.addChild(cmdCourseTxt10);

const cmdCourseTxt11 = createIntMessage(m_main_course11, 8, 328);
cmdCourseTxt11.on('pointertap',courseToMenu);
courseSelectContainer.addChild(cmdCourseTxt11);

const cmdCourseTxt12 = createIntMessage(m_main_course12, 8, 360);
cmdCourseTxt12.on('pointertap',courseToMenu);
courseSelectContainer.addChild(cmdCourseTxt12);

const cmdCourseTxt13 = createIntMessage(m_main_course13, 8, 392);
cmdCourseTxt13.on('pointertap',courseToMenu);
courseSelectContainer.addChild(cmdCourseTxt13);

const cmdCourseTxt14 = createIntMessage(m_main_course14, 8, 424);
cmdCourseTxt14.on('pointertap',courseToMenu);
courseSelectContainer.addChild(cmdCourseTxt14);

const cmdCourseTxt15 = createIntMessage(m_main_course15, 8, 460);
cmdCourseTxt15.on('pointertap',courseToMenu);
courseSelectContainer.addChild(cmdCourseTxt15);

                    



////////

function cmdMenuInteractiveOn() {
    cmdMenuTxt1.interactive = true;
    cmdMenuTxt2.interactive = true;
    cmdMenuTxt3.interactive = true;
    cmdMenuTxt4.interactive = true;
    cmdMenuTxt5.interactive = true;
}
    
function cmdMenuInteractiveOff() {
    cmdMenuTxt1.interactive = false;
    cmdMenuTxt2.interactive = false;
    cmdMenuTxt3.interactive = false;
    cmdMenuTxt4.interactive = false;
    cmdMenuTxt5.interactive = false;
}
    


app.loader
.add('img/sprite.json')
.load(onAssetLoaded);

var myimage;
var actorWlk;
var actorAtk;
var actorSet;
var actorDead;
var sra1;
var sra2;
var sra3;
var sra4;
var sra5;
var capsuleSpin;
var capsuleOpen;
var charg_gold;
var bed;
var myimageButton;
var loginButton;
var createButton;
var create2Button;
var cancelButton;
var title;
var withdraw;

function onAssetLoaded() {
    // load image and screate sprite
    let title_tex = new PIXI.Texture.from(`title_miniquest`);
    title = new PIXI.Sprite(title_tex);
    title.anchor.set(0.5);
    title.x = app.stage.width / 2;
    title.y = 0;
    title.scale.x = 1;
    title.scale.y = 1.3;

    let login_tex = new PIXI.Texture.from(`login`);
    loginButton = new PIXI.Sprite(login_tex);
    loginButton.anchor.set(0.5);
    loginButton.x = app.stage.width  / 3 + 16;
    loginButton.y = app.stage.height / 3 * 2 + 16;
    loginButton.scale.x = 0.8;
    loginButton.scale.y = 0.8;
    loginButton.interactive = true;
    loginButton.buttonMode = true;
    loginButton.on('pointertap', doLogin);
    openingContainer.addChild(loginButton);

    let withdraw_tex = new PIXI.Texture.from(`withdraw`);
    withdrawButton = new PIXI.Sprite(withdraw_tex);
    withdrawButton.anchor.set(0.5);
    withdrawButton.x = app.stage.width  / 20 * 17 + 16;
    withdrawButton.y = app.stage.height / 20 * 1;
    withdrawButton.scale.x = 0.8;
    withdrawButton.scale.y = 0.8;
    withdrawButton.interactive = true;
    withdrawButton.buttonMode = true;
    withdrawButton.on('pointertap', delete_user);
    menuContainer.addChild(withdrawButton);
    
    let create_tex = new PIXI.Texture.from(`create`);
    createButton = new PIXI.Sprite(create_tex);
    createButton.anchor.set(0.5);
    createButton.x = app.stage.width  / 3 * 2 - 16;
    createButton.y = app.stage.height / 3 * 2 + 16;
    createButton.scale.x = 0.8;
    createButton.scale.y = 0.8;
    createButton.interactive = true;
    createButton.buttonMode = true;
    createButton.on('pointertap', doCreateAccount);
    openingContainer.addChild(createButton);
    
    let create2_tex = new PIXI.Texture.from(`create2`);
    create2Button = new PIXI.Sprite(create2_tex);
    create2Button.anchor.set(0.5);
    create2Button.x = app.stage.width  / 3 + 16;
    create2Button.y = app.stage.height / 3 * 2 + 16;
    create2Button.scale.x = 0.8;
    create2Button.scale.y = 0.8;
    create2Button.interactive = true;
    create2Button.buttonMode = true;
    create2Button.on('pointertap', doCreate);
    
    let cancel_tex = new PIXI.Texture.from(`cancel`);
    cancelButton = new PIXI.Sprite(cancel_tex);
    cancelButton.anchor.set(0.5);
    cancelButton.x = app.stage.width  / 3 * 2 - 16;
    cancelButton.y = app.stage.height / 3 * 2 + 16;
    cancelButton.scale.x = 0.8;
    cancelButton.scale.y = 0.8;
    cancelButton.interactive = true;
    cancelButton.buttonMode = true;
    cancelButton.on('pointertap', doCancelCreate);

    let myimageB_tex = new PIXI.Texture.from(`myimage`);
    myimageButton = new PIXI.Sprite(myimageB_tex);
    myimageButton.anchor.set(0.5);
    myimageButton.x = app.stage.width  / 2 * 1 - 32;
    myimageButton.y = app.stage.height / 5 * 4 + 16;
    myimageButton.scale.x = 0.8;
    myimageButton.scale.y = 0.8;
    myimageButton.interactive = true;
    myimageButton.buttonMode = true;
    myimageButton.on('pointertap', uploadFile);

    let myimage_tex = new PIXI.Texture.from(`miniq01`);
    myimage = new PIXI.Sprite(myimage_tex);
    myimage.anchor.set(0.5);
    myimage.x = app.stage.width  / 5 * 4 - 32;
    myimage.y = app.stage.height / 5 * 4 + 16;
    myimage.scale.x = 1;
    myimage.scale.y = 1;
    myimage.interactive = true;
    myimage.buttonMode = true;
    myimage.on('pointertap', uploadFile);
    
    const frames = [];
    for (let i = 1; i < 3; i++){
        const val = i < 10 ? `0${i}` : i;
        frames.push(PIXI.Texture.from(`miniq${val}`));
    }
    actorWlk = new PIXI.AnimatedSprite(frames);
    actorWlk.x = app.screen.width - (app.screen.width / 3);
    actorWlk.y = app.screen.height / 2;
    actorWlk.anchor.set(0.5);
    actorWlk.animationSpeed = 0.05;
    actorWlk.zIndex = 20;
    actorWlk.scale.x = 2;
    actorWlk.scale.y = 2;
    actorWlk.play();

    // enable interactive mode
    actorWlk.interactive = true;

    // set mouse coursor to pointer when overlaped image with coursor
    actorWlk.buttonMode = true;

    battleContainer.addChild(actorWlk);
    menuContainer.addChild(actorWlk);

    const frames1 = [];
    for (let i = 5; i < 7; i++){
        const val = i < 10 ? `0${i}` : i;
        frames1.push(PIXI.Texture.from(`miniq${val}`));
    }
    actorAtk = new PIXI.AnimatedSprite(frames1);
    actorAtk.x = app.screen.width - (app.screen.width / 3);
    actorAtk.y = app.screen.height / 2;
    actorAtk.anchor.set(0.5);
    actorAtk.animationSpeed = 0.3;
    actorAtk.zIndex = 20;
    actorAtk.scale.x = 2;
    actorAtk.scale.y = 2;
    battleContainer.addChild(actorAtk);
    actorAtk.alpha = 0;

    const frames2 = [];
    for (let i = 3; i < 5; i++){
        const val = i < 10 ? `0${i}` : i;
        frames2.push(PIXI.Texture.from(`miniq${val}`));
    }
    actorSet = new PIXI.AnimatedSprite(frames2);
    actorSet.x = app.screen.width - (app.screen.width / 3);
    actorSet.y = app.screen.height / 2;
    actorSet.anchor.set(0.5);
    actorSet.animationSpeed = 0.1;
    actorSet.zIndex = 20;
    actorSet.scale.x = 2;
    actorSet.scale.y = 2;
    battleContainer.addChild(actorSet);
    actorSet.alpha = 0;

    const frames3 = [];
    for (let i = 9; i < 10; i++){
        const val = i < 10 ? `0${i}` : i;
        frames3.push(PIXI.Texture.from(`miniq${val}`));
    }
    actorDead = new PIXI.AnimatedSprite(frames3);
    actorDead.x = app.screen.width - (app.screen.width / 3);
    actorDead.y = app.screen.height / 2;
    actorDead.anchor.set(0.5);
    actorDead.animationSpeed = 0.01;
    actorDead.zIndex = 20;
    actorDead.scale.x = 2.5;
    actorDead.scale.y = 2.5;
    battleContainer.addChild(actorDead);
    actorDead.alpha = 0;

    const sra1frames = [];
    for (let i = 1; i < 3; i++){
        const val = i < 10 ? `0${i}` : i;
        sra1frames.push(PIXI.Texture.from(`sra${val}`));
    }
    sra1 = new PIXI.AnimatedSprite(sra1frames);
    sra1.x = app.screen.width / 3;
    sra1.y = app.screen.height / 2;
    sra1.anchor.set(0.5);
    sra1.animationSpeed = 0.05;
    sra1.zIndex = 15;
    sra1.scale.x = 2;
    sra1.scale.y = 2;
    battleContainer.addChild(sra1);
    sra1.alpha = 0;
    sra1.play();

    
    const sra2frames = [];
    for (let i = 3; i < 5; i++){
        const val = i < 10 ? `0${i}` : i;
        sra2frames.push(PIXI.Texture.from(`sra${val}`));
    }
    sra2 = new PIXI.AnimatedSprite(sra2frames);
    sra2.x = app.screen.width / 3;
    sra2.y = app.screen.height / 2;
    sra2.anchor.set(0.5);
    sra2.animationSpeed = 0.05;
    sra2.zIndex = 15;
    sra2.scale.x = 2;
    sra2.scale.y = 2;
    battleContainer.addChild(sra2);
    sra2.alpha = 0;
    sra2.play();

    const sra3frames = [];
    for (let i = 5; i < 7; i++){
        const val = i < 10 ? `0${i}` : i;
        sra3frames.push(PIXI.Texture.from(`sra${val}`));
    }
    sra3 = new PIXI.AnimatedSprite(sra3frames);
    sra3.x = app.screen.width / 3;
    sra3.y = app.screen.height / 2;
    sra3.anchor.set(0.5);
    sra3.animationSpeed = 0.05;
    sra3.zIndex = 15;
    sra3.scale.x = 2;
    sra3.scale.y = 2;
    battleContainer.addChild(sra3);
    sra3.alpha = 0;
    sra3.play();

    const sra4frames = [];
    for (let i = 7; i < 9; i++){
        const val = i < 10 ? `0${i}` : i;
        sra4frames.push(PIXI.Texture.from(`sra${val}`));
    }
    sra4 = new PIXI.AnimatedSprite(sra4frames);
    sra4.x = app.screen.width / 3;
    sra4.y = app.screen.height / 2;
    sra4.anchor.set(0.5);
    sra4.animationSpeed = 0.05;
    sra4.zIndex = 15;
    sra4.scale.x = 2;
    sra4.scale.y = 2;
    battleContainer.addChild(sra4);
    sra4.alpha = 0;
    sra4.play();

    const sra5frames = [];
    for (let i = 9; i < 11; i++){
        const val = i < 10 ? `0${i}` : i;
        sra5frames.push(PIXI.Texture.from(`sra${val}`));
    }
    sra5 = new PIXI.AnimatedSprite(sra5frames);
    sra5.x = app.screen.width / 3;
    sra5.y = app.screen.height / 2;
    sra5.anchor.set(0.5);
    sra5.animationSpeed = 0.05;
    sra5.zIndex = 15;
    sra5.scale.x = 2;
    sra5.scale.y = 2;
    battleContainer.addChild(sra5);
    sra5.alpha = 0;
    sra5.play();

    const capsuleMachineframes1 = [];
    for (let i = 1; i < 3; i++){
        const val = i < 10 ? `0${i}` : i;
        capsuleMachineframes1.push(PIXI.Texture.from(`gacha${val}`));
    }

    capsuleMachine = new PIXI.AnimatedSprite(capsuleMachineframes1);
    capsuleMachine.x = app.screen.width / 2;
    capsuleMachine.y = app.screen.height / 3 + 24;
    capsuleMachine.anchor.set(0.5);
    capsuleMachine.animationSpeed = 0.1;
    capsuleMachine.zIndex = 10;
    capsuleMachine.scale.x = 1;
    capsuleMachine.scale.y = 1;
    gachaContainer.addChild(capsuleMachine);
    capsuleMachine.alpha = 1;
    capsuleMachine.stop();

    const arakureframes1 = [];
    for (let i = 2; i < 3; i++){
        const val = i < 10 ? `0${i}` : i;
        arakureframes1.push(PIXI.Texture.from(`arakure${val}`));
    }

    arakure = new PIXI.AnimatedSprite(arakureframes1);
    arakure.x = (app.screen.width / 3) * 2;
    arakure.y = app.screen.height / 2;
    arakure.anchor.set(0.5);
    arakure.animationSpeed = 0.1;
    arakure.zIndex = 10;
    arakure.scale.x = 2;
    arakure.scale.y = 2;
    gachaContainer.addChild(arakure);
    arakure.alpha = 1;
    arakure.stop();

    const armour01frames = [];
    for (let i = 1; i < 2; i++){
        const val = i < 10 ? `0${i}` : i;
        armour01frames.push(PIXI.Texture.from(`armour${val}`));
    }
    armour01 = new PIXI.AnimatedSprite(armour01frames);
    armour01.x = app.screen.width / 2;
    armour01.y = app.screen.height / 2 - 16;
    armour01.anchor.set(0.5);
    armour01.animationSpeed = 0.2;
    armour01.zIndex = 15;
    armour01.scale.x = 2;
    armour01.scale.y = 2;
    armour01.alpha = 0;
    armour01.stop();

    const weapon01frames = [];
    for (let i = 1; i < 2; i++){
        const val = i < 10 ? `0${i}` : i;
        weapon01frames.push(PIXI.Texture.from(`weapon${val}`));
    }
    weapon01 = new PIXI.AnimatedSprite(weapon01frames);
    weapon01.x = app.screen.width / 2;
    weapon01.y = app.screen.height / 2 - 16;
    weapon01.anchor.set(0.5);
    weapon01.animationSpeed = 0.2;
    weapon01.zIndex = 15;
    weapon01.scale.x = 2;
    weapon01.scale.y = 2;
    weapon01.alpha = 0;
    weapon01.stop();

    const capsuleSpinframes1 = [];
    for (let i = 1; i < 12; i++){
        const val = i < 10 ? `0${i}` : i;
        capsuleSpinframes1.push(PIXI.Texture.from(`capsule${val}`));
    }
    capsuleSpin = new PIXI.AnimatedSprite(capsuleSpinframes1);
    capsuleSpin.x = app.screen.width / 2;
    capsuleSpin.y = app.screen.height / 2;
    capsuleSpin.anchor.set(0.5);
    capsuleSpin.animationSpeed = 0.2;
    capsuleSpin.zIndex = 15;
    capsuleSpin.scale.x = 1;
    capsuleSpin.scale.y = 1;
    gachaContainer.addChild(capsuleSpin);
    capsuleSpin.alpha = 0;
    capsuleSpin.stop();

    const capsuleOpen1frames = [];
    for (let i = 12; i < 13; i++){
        const val = i < 10 ? `0${i}` : i;
        capsuleOpen1frames.push(PIXI.Texture.from(`capsule${val}`));
    }
    capsuleOpen1 = new PIXI.AnimatedSprite(capsuleOpen1frames);
    capsuleOpen1.x = app.screen.width / 2;
    capsuleOpen1.y = app.screen.height / 2;
    capsuleOpen1.anchor.set(0.5);
    capsuleOpen1.animationSpeed = 0.2;
    capsuleOpen1.zIndex = 25;
    capsuleOpen1.scale.x = 3.3;
    capsuleOpen1.scale.y = 3.3;
    capsuleOpen1.alpha = 0;

    const capsuleOpen2frames = [];
    for (let i = 13; i < 14; i++){
        const val = i < 10 ? `0${i}` : i;
        capsuleOpen2frames.push(PIXI.Texture.from(`capsule${val}`));
    }
    capsuleOpen2 = new PIXI.AnimatedSprite(capsuleOpen2frames);
    capsuleOpen2.x = app.screen.width / 2;
    capsuleOpen2.y = app.screen.height / 2;
    capsuleOpen2.anchor.set(0.5);
    capsuleOpen2.animationSpeed = 0.2;
    capsuleOpen2.zIndex = 20;
    capsuleOpen2.scale.x = 3.3;
    capsuleOpen2.scale.y = 3.3;
    capsuleOpen2.alpha = 0;

    gachaContainer.addChild(capsuleOpen2);
    gachaContainer.addChild(armour01);
    gachaContainer.addChild(weapon01);
    gachaContainer.addChild(capsuleOpen1);

    const coinframes = [];
    for (let i = 1; i < 2; i++){
        const val = i < 10 ? `0${i}` : i;
        coinframes.push(PIXI.Texture.from(`coin${val}`));
    }
    coin = new PIXI.AnimatedSprite(coinframes);
    coin.x = app.screen.width / 2;
    coin.y = app.screen.height / 3;
    coin.anchor.set(0.5);
    coin.animationSpeed = 0.2;
    coin.zIndex = 25;
    coin.scale.x = 1;
    coin.scale.y = 1;
    coin.alpha = 0;
    gachaContainer.addChild(coin);

    const star1frames = [];
    for (let i = 1; i < 2; i++){
        const val = i < 10 ? `0${i}` : i;
        star1frames.push(PIXI.Texture.from(`star${val}`));
    }
    star1 = new PIXI.AnimatedSprite(star1frames);
    star1.x = app.screen.width / 2 + 16;
    star1.y = app.screen.height / 2 + 16;
    star1.anchor.set(0.5);
    star1.animationSpeed = 0.2;
    star1.zIndex = 25;
    star1.scale.x = 0.5;
    star1.scale.y = 0.5;
    star1.alpha = 0;
    gachaContainer.addChild(star1);

    const star2frames = [];
    for (let i = 1; i < 2; i++){
        const val = i < 10 ? `0${i}` : i;
        star2frames.push(PIXI.Texture.from(`star${val}`));
    }
    star2 = new PIXI.AnimatedSprite(star2frames);
    star2.x = app.screen.width / 2;
    star2.y = app.screen.height / 2 + 16;
    star2.anchor.set(0.5);
    star2.animationSpeed = 0.2;
    star2.zIndex = 25;
    star2.scale.x = 0.5;
    star2.scale.y = 0.5;
    star2.alpha = 0;
    gachaContainer.addChild(star2);

    const star3frames = [];
    for (let i = 1; i < 2; i++){
        const val = i < 10 ? `0${i}` : i;
        star3frames.push(PIXI.Texture.from(`star${val}`));
    }
    star3 = new PIXI.AnimatedSprite(star3frames);
    star3.x = app.screen.width / 2 - 16;
    star3.y = app.screen.height / 2 + 16;
    star3.anchor.set(0.5);
    star3.animationSpeed = 0.2;
    star3.zIndex = 25;
    star3.scale.x = 0.5;
    star3.scale.y = 0.5;
    star3.alpha = 0;
    gachaContainer.addChild(star3);

    const bedframes1 = [];
    for (let i = 1; i < 2; i++){
        const val = i < 10 ? `0${i}` : i;
        bedframes1.push(PIXI.Texture.from(`bed${val}`));
    }
    bed = new PIXI.AnimatedSprite(bedframes1);
    bed.x = app.screen.width / 2;
    bed.y = app.screen.height / 2 - 24;
    bed.anchor.set(0.5);
    bed.animationSpeed = 0.1;
    bed.zIndex = 10;
    bed.scale.x = 0.8;
    bed.scale.y = 0.8;
    staminaContainer.addChild(bed);
    bed.alpha = 1;
    bed.stop();

    const charge_goldframes1 = [];
    for (let i = 1; i < 2; i++){
        const val = i < 10 ? `0${i}` : i;
        charge_goldframes1.push(PIXI.Texture.from(`charge_gold${val}`));
    }
    charge_gold = new PIXI.AnimatedSprite(charge_goldframes1);
    charge_gold.x = app.screen.width / 2;
    charge_gold.y = app.screen.height / 2;
    charge_gold.anchor.set(0.5);
    charge_gold.animationSpeed = 0.1;
    charge_gold.zIndex = 10;
    charge_gold.scale.x = 1;
    charge_gold.scale.y = 1;
    chargeContainer.addChild(charge_gold);
    charge_gold.alpha = 1;
    charge_gold.stop();



} // end of function


/** =======================================================================================
 * 
 */

// sort from zIndex
app.stage.sortableChildren = true;

function delChildByName(container, name){
    for(i = 0; i < container.children.length; i++){
        if(container.children[i].name === name){
            container.removeChildAt(i);
        }
    }
}

