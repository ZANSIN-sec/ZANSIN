
//const m_gacha_m1 = "今回のお前の運勢はどうだろうな？  いい装備が出るといいな。";
//const m_gacha_m2 = "今回ダメでも、次はいいのがでるかもしれないぞ？";
//const m_gacha_m3 = "運が良ければ1発でSR装備が出るかもな！";
//const m_gacha_b1 = "おっと、悪い結果でも恨みっこなしだぜ？";
//const m_gacha_b2 = "俺はイカサマなんてしないからな？ 恨むならゲームの作者を恨んでくれ。";
//const m_gacha_b3 = "悪い装備ではないと思うが・・・。　次はもっといいのが出るかもな。";
//const m_gacha_s1 = "やったじゃないか。スーパーレアだな。";
//const m_gacha_s2 = "お宝装備じゃないか。　でも、次はもっといいのが出るかもしれないぞ。";
//const m_gacha_s3 = "最高だな！！お前は運がいいぞ。　もっと上を目指してみるか？";
//const m_gacha_r1 = "レアものだな。";
//const m_gacha_r2 = "なかなかの装備だぞ。　お前にはもったいないくらいだ。";
//const m_gacha_r3 = "割といいんじゃないか？　それだけ強い装備なら申し分ない。";
//const m_gacha_n1 = "今の装備より強そうだな。";
//const m_gacha_n2 = "悪くないんじゃないか？　俺も昔はその装備を使っていたさ。";
//const m_gacha_n3 = "いい装備は出たか？　次はレアものが出るかもな。";
//const m_gacha_e1 = "所持金が足りないみたいだな。　　　　いくらなんでもタダにはできないぜ。　こっちも商売なんですまんな。";
//                  1234567890123456789012345678901234567890
//                                                      1234567890123456789012345678901234567890
const m_gacha_m1 = "What's your fortune? I hope you get some better one.";
const m_gacha_m2 = "Even if you got a bad item this time, you might get a good one next time.";
const m_gacha_m3 = "You might get a amazing one with    any luck!";
const m_gacha_b1 = "Don't hold resent against me if you don't get good results.";
const m_gacha_b2 = "I'm not cheating.";
const m_gacha_b3 = "No bad. but may be get better one   next time.";
const m_gacha_s1 = "Yes!!! This is SUPER RARE!!!";
const m_gacha_s2 = "Wow. That's a treasure!";
const m_gacha_s3 = "Super!!! You're a lucky man.";
const m_gacha_r1 = "It's RARE.";
const m_gacha_r2 = "It's quite good one.　              It's too good for you. HaHa.";
const m_gacha_r3 = "Oh, You got a nice one. I want one  too.";
const m_gacha_n1 = "It looks like stronger than the     current one.";
const m_gacha_n2 = "Not bad, huh?　I was using this too.";
const m_gacha_n3 = "Did you get a good one? Maybe next  time you'll get something rare.";
const m_gacha_e1 = "You don't have enough money.";

function gachaFetch (){
    let lock = sessionStorage.getItem("lock");  
    if(lock === null || lock === "0"){
        sessionStorage.setItem("lock","1");
        console.log("lock");
        let type = 1;
        let rare = 1;
        let timer;
        let num = Math.floor(Math.random() * 10) % 3;
        if(num === 0){
            //setMessage(gacha, "今回のお前の運勢はどうだろうな？  いい装備が出るといいな。");
            setMessage(gacha, m_gacha_m1);
        } else if(num === 1){
            //setMessage(gacha, "今回ダメでも、次はいいのがでるかもしれないぞ？");
            setMessage(gacha, m_gacha_m2);
        } else if(num === 2){
            //setMessage(gacha, "運が良ければ1発でSR装備が出るかもな！");
            setMessage(gacha, m_gacha_m3);
        }

        sessionStorage.removeItem(gacha);
        action_gacha();

        let action = () => {
            setTimeout(unlock, 6500);
            let data = sessionStorage.getItem("gacha");
            if(data !== undefined) {
                clearInterval(t1);
                player();
                setTimeout(setStat, 1000);
                let j = JSON.parse(data);
                if(j.resulttype !== 1){
                    // have enough money
                    if(j.result === "ok"){
                        if(j.rarity === "N"){
                            rare = 1;
                        } else if(j.rarity === "R"){
                            rare = 2;
                        } else if(j.rarity === "SR"){
                            rare = 3;
                        } else {
                            rare = 0;
                        }
                        if(j.type === "weapon"){
                            type = 1;
                        } else {
                            type = 2;
                        }

                        setCoinDefault();
                        coin.alpha = 1;
                        let dst = coin.y + (app.screen.height / 12);
            
                        let startGatya = () => {
                            setCapsuleDefault();
                            coin.y += 4;
                            if(coin.y > dst){
                                coin.alpha = 0;
                                clearInterval(timer);
                                capsuleMachine.play();
                                setTimeout(fetch, 1000);
                            }
                        }
                        timer = setInterval(startGatya, 100);

                        let fetch = () => {
                            capsuleMachine.stop();
                            capsuleSpin.alpha = 1;
                            capsuleSpin.play();
                            timer = setInterval(scaleUp, 100);
                        };

                        let scaleUp = () => {
                            let x = capsuleSpin.scale.x;
                            if(x <= 3.3){
                                capsuleSpin.scale.x += 0.1;
                                capsuleSpin.scale.y += 0.1;
                            } else {
                                capsuleSpin.stop();
                                if(type === 1){
                                    weapon01.alpha = 1;
                                } else if(type === 2){
                                    armour01.alpha = 1;
                                }
                                capsuleOpen2.alpha = 1;
                                capsuleOpen1.alpha = 1;
                                capsuleSpin.alpha = 0;
                                if(capsuleOpen1.y > app.screen.height / 2 - 64){
                                    capsuleOpen2.y += 2;
                                    capsuleOpen1.y -= 8;
                                } else {
                                    clearInterval(timer);
                                    //let name = j.name + "じゃないか。";
                                    let name = "You got the " + j.name + ".";
                                    //for(let i = name.length + 6; i < 18; i++){
                                    for(let i = name.length + 6; i < 41; i++){
                                        name = name + " ";
                                    }
                                    num = Math.floor(Math.random() * 10) % 3;
                                    if(j.resulttype == "2"){
                                        if(num === 0){
                                            //setMessage(gacha, name + "おっと、悪い結果でも恨みっこなしだぜ？");
                                            setMessage(gacha, name + " " + m_gacha_b1);
                                        } else if(num === 1){
                                            //setMessage(gacha, name + "俺はイカサマなんてしないからな？ 恨むならゲームの作者を恨んでくれ。");
                                            setMessage(gacha, name + " " + m_gacha_b2);
                                        } else if(num === 2){
                                            //setMessage(gacha, name + "悪い装備ではないと思うが・・・。　次はもっといいのが出るかもな。");
                                            setMessage(gacha, name + " " + m_gacha_b3);
                                        }
                                    } else {
                                        if(rare === 3){
                                            if(num === 0){
                                                //setMessage(gacha, name + "やったじゃないか。スーパーレアだな。");
                                                setMessage(gacha, name + " " + m_gacha_s1);
                                            } else if(num === 1){
                                                //setMessage(gacha, name + "お宝装備じゃないか。　でも、次はもっといいのが出るかもしれないぞ。");
                                                setMessage(gacha, name + " " + m_gacha_s2);
                                            } else if(num === 2){
                                                //setMessage(gacha, name + "最高だな！！お前は運がいいぞ。　もっと上を目指してみるか？");
                                                setMessage(gacha, name + " " + m_gacha_s3);
                                            }
                                        } else if(rare === 2){
                                            if(num === 0){
                                                //setMessage(gacha, name + "レアものだな。");
                                                setMessage(gacha, name + " " + m_gacha_r1);
                                            } else if(num === 1){
                                                //setMessage(gacha, name + "なかなかの装備だぞ。　お前にはもったいないくらいだ。");
                                                setMessage(gacha, name + " " + m_gacha_r2);
                                            } else if(num === 2){
                                                //setMessage(gacha, name + "割といいんじゃないか？　それだけ強い装備なら申し分ない。");
                                                setMessage(gacha, name + " " + m_gacha_r3);
                                            }
                                        } else {
                                            if(num === 0){
                                                //setMessage(gacha, name + "今の装備より強そうだな。");
                                                setMessage(gacha, name + " " + m_gacha_n1);
                                            } else if(num === 1){
                                                //setMessage(gacha, name + "悪くないんじゃないか？　俺も昔はその装備を使っていたさ。");
                                                setMessage(gacha, name + " " + m_gacha_n2);
                                            } else if(num === 2){
                                                //setMessage(gacha, name + "いい装備は出たか？　次はレアものが出るかもな。");
                                                setMessage(gacha, name + " " + m_gacha_n3);
                                            }
                                        }
                                    }
                                    switch(rare){
                                        case 3:
                                            star3.alpha = 1;
                                        case 2:
                                            star2.alpha = 1;
                                        case 1:
                                            star1.alpha = 1;
                                        default:
                                    }
                                }
                            }
                        };
                    }
                } else {
                    //setMessage(gacha, "所持金が足りないみたいだな。　　　　いくらなんでもタダにはできないぜ。　こっちも商売なんですまんな。");
                    setMessage(gacha, m_gacha_e1);
                }
            } // sessionStorage undef
        };
        let unlock = () => {
            sessionStorage.setItem("lock", "0");
            console.log("unlock");
        }
        let t1 = setInterval(action, 300);
    }
}


function setCapsuleDefault(){
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
    capsuleOpen1.x = app.screen.width / 2;
    capsuleOpen1.y = app.screen.height / 2;
    capsuleOpen1.anchor.set(0.5);
    capsuleOpen1.animationSpeed = 0.2;
    capsuleOpen1.zIndex = 25;
    capsuleOpen1.scale.x = 3.3;
    capsuleOpen1.scale.y = 3.3;
    capsuleOpen1.alpha = 0;
    capsuleOpen2.x = app.screen.width / 2;
    capsuleOpen2.y = app.screen.height / 2;
    capsuleOpen2.anchor.set(0.5);
    capsuleOpen2.animationSpeed = 0.2;
    capsuleOpen2.zIndex = 25;
    capsuleOpen2.scale.x = 3.3;
    capsuleOpen2.scale.y = 3.3;
    capsuleOpen2.alpha = 0;
    weapon01.alpha = 0;
    armour01.alpha = 0;
    star1.alpha = 0;
    star2.alpha = 0;
    star3.alpha = 0;
}

function setCoinDefault(){
  coin.x = app.screen.width / 2;
  coin.y = app.screen.height / 3;
  coin.anchor.set(0.5);
  coin.animationSpeed = 0.2;
  coin.zIndex = 25;
  coin.scale.x = 1;
  coin.scale.y = 1;
  coin.alpha = 0;
}

