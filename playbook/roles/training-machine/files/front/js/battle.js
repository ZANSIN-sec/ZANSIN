const m_battle_select  = 'Command?';
const m_battle_defence = 'is defending.';
const m_battle_magic   = 'My goodness, no spells is implemented!';
const m_battle_runaway = 'run away.';
//
/////////
//
function doBattle(){

    let setupStop = () => {
        orig.stop()
        setup.stop();
    }
    let attackStop = () => {
        attack.stop();
    }
    let attackReset = () => {
        orig.alpha = 1;
        attack.alpha = 0;
        orig.alpha = 1;
        orig.play();
    }
    let dead = () => {
        orig.alpha = 0;
        attack.alpha = 0;
        actorDead.alpha = 1;
    }
    let attackAction = () => {
        setup.alpha = 0;
        attack.alpha = 1;
        attack.play();
        setTimeout(attackStop, 500);
        // action
        TweenMax.to(attack, 0.5, 
                {   
                    pixi: { 
                        x: attack.x - app.screen.width / 3, 
                    },
                    ease: Power0.easeNone, 
                    repeat: 1,
                    yoyo: true
                }
            );
        if(sessionStorage.battle.status.result === "lose") {
            setTimeout(dead, 1500);
        } else {
            setTimeout(attackReset, 1500);
        }
    }
    
    let orig = actorWlk;
    orig.alpha = 0;

    let setup = actorSet;
    setup.alpha = 1;
    setup.play();
    setTimeout(setupStop, 250);
    setTimeout(attackAction, 1000);
    setTimeout(action_attack, 1200);

    let attack = actorAtk;

}

function doGuard(){
    let name = (JSON.parse(sessionStorage.pinfo)).nick_name;
    clearMessage(battle);
    //setMessage(battle, name + 'はぼうぎょしている。');
    setMessage(battle, name + ' ' + m_battle_defence);
}

function doMagic(){
    clearMessage(battle);
    //setMessage(battle, 'なんと、まほうは実装されていない！');
    setMessage(battle, m_battle_magic);
}

function doEscape(){
    let name = (JSON.parse(sessionStorage.pinfo)).nick_name;
    let goToMenu = () => {
        battleContainer = app.stage.removeChild(battleContainer);
        modeMenu();
        clearMessage(battle);
        //setMessage(menu, 'メニューから行動を選択してください。');
        setMessage(menu, m_battle_select);
        sra1.alpha = 0;
        sra2.alpha = 0;
        sra3.alpha = 0;
        sra4.alpha = 0;
        sra5.alpha = 0;
    };

    //setMessage(battle, name + 'はにげだした！');
    setMessage(battle, name + ' ' + m_battle_runaway);
    setTimeout(goToMenu, 800);
}
