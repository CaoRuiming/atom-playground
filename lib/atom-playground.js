'use babel';

import fs from 'fs';
import { CompositeDisposable, BufferedProcess } from 'atom';
import Utils from './utils';

export default {

  subscriptions: null,
	subscribedEvent: null,

  activate(state) {
    this.subscriptions = new CompositeDisposable();

    this.subscriptions.add(atom.commands.add('atom-workspace', {
      'atom-playground:toggle': () => { this.toggle(); }
    }));

		this.evaluate();
  },

  deactivate() {
    this.subscriptions.dispose();
  },

  serialize() {
    return {};
  },

	createEventListener() {
		let editor;
		if (editor = atom.workspace.getActiveTextEditor()) {
			return editor.getBuffer().onDidStopChanging((event) => { this.evaluate(); });
		}
		else { throw `No active Atom Text Editor detected!`; }
	},

	toggle() {
		if (this.subscribedEvent) {
			this.subscriptions.remove(this.subscribedEvent);
			this.subscribedEvent.dispose();
			this.subscribedEvent = null;
		}
		else {
			this.subscribedEvent = this.createEventListener();
			this.subscriptions.add(this.subscribedEvent);
		}
	},

  evaluate() {
		let editor;
		if (editor = atom.workspace.getActiveTextEditor()) {
			let language = editor.getGrammar().name;

			if (language == `JavaScript`) { this.evaluateJavaScript(editor); }
			else if (language == `Swift`) { this.evaluateSwift(editor); }
			else if (language == `Python`) { this.evaluatePython(editor); }
			else{
				const error = `${language} is not supported (╯°□°）╯︵ ┻━┻`;
				atom.notifications.addWarning(error);
			}
		}
  },

	evaluateJavaScript(editor) {
		let expression = editor.getSelectedText();
		let output;
		let evaluation;
		if (evaluation = eval(expression)) { output = ` // ${evaluation}`; }
		else { output = ``; }
		editor.moveRight();
		editor.moveLeft();
		editor.moveToEndOfLine();
		editor.insertText(output);
	},

	evaluateSwift(editor) {
		const outputDir = `${atom.getConfigDirPath()}/.atom-playground`;
		if (!fs.existsSync(outputDir)) { fs.mkdir(outputDir); }
		const inputFilePath = `${outputDir}/input.swift`;
		const outputFilePath = `${outputDir}/Swift Output`;
		fs.writeFile(inputFilePath, editor.getText(), 'utf8', (error) => {
			if (error) throw error;
		});

		const stdout = (output) => {
			return fs.writeFile(outputFilePath, output, 'utf8', (error) => {
				if (error) { atom.notifications.addWarning(error); throw error; }
				const activePane = atom.workspace.getActivePane();
				return atom.workspace.open(outputFilePath, {split: 'right', activatePane: false}).then(newEditor => activePane.activate());
			});
		};
		return new BufferedProcess({
			command: `xcrun`,
			args: [`swift`, inputFilePath],
			stdout: stdout,
			stderr: stdout
		});
	},

	evaluatePython(editor) {
		const outputDir = `${atom.getConfigDirPath()}/.atom-playground`;
		if (!fs.existsSync(outputDir)) { fs.mkdir(outputDir); }
		const inputFilePath = `${outputDir}/input.py`;
		const outputFilePath = `${outputDir}/Python Output`;
		fs.writeFile(inputFilePath, editor.getText(), 'utf8', (error) => {
			if (error) throw error;
		})

		const stdout = (output) => {
			return fs.writeFile(outputFilePath, output, 'utf8', (error) => {
				if (error) { atom.notifications.addWarning(error); throw error; }
				const activePane = atom.workspace.getActivePane();
				return atom.workspace.open(outputFilePath, {split: 'right', activatePane: false}).then(newEditor => activePane.activate());
			});
		};
		interpreterDir = `${atom.packages.getPackageDirPaths()[0]}/atom-playground`
		return new BufferedProcess({
			command: `python`,
			args: [`${interpreterDir}/lib/interpreters/python/main.py`, inputFilePath],
			stdout: stdout,
			stderr: stdout
		});
	}

};
