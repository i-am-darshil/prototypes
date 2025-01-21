function generateRandomWord(length: number): string {
  const characters = "abcdefghijklmnopqrstuvwxyz";
  let word = "";
  for (let i = 0; i < length; i++) {
    const randomIndex = Math.floor(Math.random() * characters.length);
    word += characters[randomIndex];
  }
  return word;
}

function generateRandomWords(count: number, wordLength: number): string {
  const words: string[] = [];
  for (let i = 0; i < count; i++) {
    words.push(generateRandomWord(wordLength));
  }
  return words.join("-");
}


export {
  generateRandomWords
}