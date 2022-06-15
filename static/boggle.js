class BoggleGame {
    constructor(boardId, gameLength = 60) {
      this.gameLength = gameLength;
      this.showTimer();
      this.score = 0;
      this.words = new Set();
      this.board = $("#" + boardId);
      this.timer = setInterval(this.gameTick.bind(this), 1000);
      $(".add-word", this.board).on("submit", this.submit.bind(this));
    }
  
    displayWord(word) {
      $(".words", this.board).append($("<li>", { text: word }));
    }
    
    displayScore() {
      $(".score", this.board).text(this.score);
    }
  
    displayMessage(message, cls) {
      $(".message", this.board)
        .text(message)
        .removeClass()
        .addClass(`message ${cls}`);
    }
  
    async submit(evt) {
      console.log('submit function');
      evt.preventDefault();
      const showWord = $(".word", this.board);

      let word = showWord.val();
      if (!word) return;
  
      if (this.words.has(word)) {
        this.displayMessage("This word already exists");
        return;
      }
      
      const response = await axios.get("/word-check", { params: { word: word }});
      if (response.data.result === "not-word") {
        this.displayMessage(`${word} is not an english word`);
      } 
      else if (response.data.result === "not-on-board") {
        this.displayMessage(`${word} is not valid for this board`);
      } 
      else {
        this.displayWord(word);
        this.score += word.length;
        this.displayScore();
        this.words.add(word);
        this.displayMessage(`Added ${word}`);
      }
  
      showWord.val("").focus();
    }
  
    showTimer() {
      $(".timer", this.board).text(this.gameLength);
    }
  
    async gameTick() {
      this.gameLength -= 1;
      this.showTimer();
  
      if (this.gameLength === 0) {
        clearInterval(this.timer);
        await this.scoreGame();
      }
    }
  
    async scoreGame() {
      $(".add-word", this.board).hide();
      const response = await axios.get("/score", { score: this.score });
      this.displayMessage(`Final score: ${this.score}`);
    }
  }