'use babel';

export default class Utils {

	// given a String representing a file path, returns the path of
	// the parent directory
	static getParentDir(dir) {
		while (dir.substring(dir.length-1) != `/`) {
			dir = dir.substring(0, dir.length-1)
		}
		return dir.substring(0, dir.length-1)
	}

}
