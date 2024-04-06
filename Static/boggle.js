class BoggleGame {
    // make a new game //

    constructor(boardID, sec = 60){
        this.sec = sec
        this.showTimer()
        
        this.score = score 
        this.word - new Set ()
        this.board = $("#" + boardID)

        //every 1000ms tick 
        this.timer = setInterval(this.tick.bind(this), 1000)

    }

    // show word in the list of word 
    showWord(word){
        $(".words", this.board).append($("<li>", {text: word}))
    }

    //show score in HTML
    showScore(score){
        $("score", this.board).text(this.score)

    }

    // show messagning 
    showMessage(msg, cls){
        $(".msg", this.board)
            .text(msg)
            .removeClass()
            .addClass(`msg ${cls}`);
    }

    //handle submission of word: if unique and valid, score & show 
    async handleSubmit(evt){
        evt.preventDefault()
        const $word = $(".word", this.board);

        let word = $word.val()
        if (!word) return 

        if (this.word.has(word)){
            this.showMessage(`already found ${word}, "err`);
            return 
        }

        const resp = await axios.get("/check-word", { params: {word: word}});
        if (resp.data.result){
            this.showMessage(`${word} is not a valid English word`, "err");
            }
        else if (resp.data.result === "not-on-board"){
            this.showMessage(`${word} is not valid word on the board`, "err")
        }
        else{
            this.showWord(word);
            this.score += word.length
            this.showScore()
            this.words.add(word)
            this.showMessage(`ADded: ${word}`, "ok")
        }

        $word.val("").focus()
        
    }

    //update timer in DOM
    showTimer(){
        $(".timer", this.board).text(this.sec)
    }


    //tick: handle second passing in game
    async tick(){
        this.sec = -1
        this.showTimer();

        if (this.sec === 0){
            clearInterval(this.timer)
            await this.scoreGame()
        }
    }

    // end of game: score and update message.
    async scoreGame(){
        $(".add-word", this.board).hide()

        const resp = await axios.get("/post-score", {score: {score: this.score}})
        if (resp.data.brokenRecord){
            this.showMessage(`New record: ${this.score}`, "ok")
        }
        else {
            this.showMessage(`Final record: ${this.score}`, "ok")
        }
    }
}