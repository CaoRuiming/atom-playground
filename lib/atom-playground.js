'use babel';

import fs from 'fs';
//import AtomPlaygroundView from './atom-playground-view';
import { CompositeDisposable, BufferedProcess } from 'atom';

export default {

  subscriptions: null,

  activate(state) {
    // Events subscribed to in atom's system can be easily cleaned up with a CompositeDisposable
    this.subscriptions = new CompositeDisposable();

    // Register command that toggles this view
    this.subscriptions.add(atom.commands.add('atom-workspace', {
      'atom-playground:fetch': () => this.fetch()
    }));
  },

  deactivate() {
    this.subscriptions.dispose();
  },

  serialize() {
    return {};
  },

  fetch() {
		let editor
		if (editor = atom.workspace.getActiveTextEditor()) {
			let language = editor.getGrammar().name
			console.log(`evaluating ${language}`)

			if (language == 'JavaScript') { this.evaluateJavaScript(editor) }
			else if (language == 'Swift') { this.evaluateSwift(editor) }
			else{
				const error = `${language} is not supported (╯°□°）╯︵ ┻━┻`
				atom.notifications.addWarning(error)
			}
		}
  },

	evaluateJavaScript(editor) {
		let expression = editor.getSelectedText()
		let output
		let evaluation
		if (evaluation = eval(expression)) { output = ' // ' + evaluation }
		else { output = '' }
		editor.moveRight()
		editor.moveLeft()
		editor.moveToEndOfLine()
		editor.insertText(output)
	},

	evaluateSwift(editor) {
		const outputDir = `${atom.getConfigDirPath()}/.swift-playground`
		if (!fs.existsSync(outputDir)) { fs.mkdir(outputDir) }
		const inputFilePath = `${outputDir}/input.swift`
		const outputFilePath = `${outputDir}/Swift Output`
		fs.writeFile(inputFilePath, editor.getText(), 'utf8', (error) => {
			if (error) throw error;
			console.log(`Saved Input File Successfully!`)
		})

		const stdout = (output) => {
			return fs.writeFile(outputFilePath, output, 'utf8', (error) => {
				if (error) { atom.notifications.addWarning(error); throw error; }
				const activePane = atom.workspace.getActivePane()
				return atom.workspace.open(outputFilePath, {split: 'right', activatePane: false}).then(newEditor => activePane.activate())
			})
		}
		return new BufferedProcess({
			command: "xcrun",
			args: ["swift", inputFilePath],
			stdout: stdout,
			stderr: stdout
		})
	}

};
