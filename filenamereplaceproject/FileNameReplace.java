/**
 * 
 */
package filenamereplaceproject;

import java.io.File;
import java.nio.file.Path;
import java.nio.file.Paths;


/**
 * @author t-ishigaki
 *
 */
public class FileNameReplace {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		String dir = args[0];
//		String dir = "C:\\Users\\t-ishigaki\\Desktop\\開発\\tmp";
		String targetStr = args[1];
		String newStr = args[2];
		
		File filePaths[] = getFilePaths(dir);
		renameFilename(filePaths,dir,targetStr,newStr);
	}
	
	
	/**
	 * ファイル一覧を取得
	 * @param dir
	 * @retunr file
	 */
	public static File[] getFilePaths(String dir) {
		File dirPath = new File(dir);
		File filePaths[] = dirPath.listFiles();
		return filePaths;
	}
	
	
	/**
	 * ファイル一覧から対象ファイルをリネーム
	 * @param filePaths
	 * @param targetDir
	 * @param targetStr
	 * @param newStr
	 */
	public static void renameFilename(File filePaths[],String targetDir,String targetStr,String newStr) {
		for(File path : filePaths) {
			String filename = path.getName();
			if(filename.contains(targetStr)) {
				String newFilename = filename.replace(targetStr,newStr);
				renameFilename(targetDir,filename,newFilename);
			}
		}
	}
	
	/**
	 * ファイルオブジェクトを作成
	 * @param dir
	 * @param filename
	 * @retunr file
	 */
	public static File createFileObj(String dir,String filename) {
		Path path = Paths.get(dir,filename);
		File file = path.toFile();
		return file;
	}
	
	/**
	 * ファイルをリネーム
	 * @param targetDir
	 * @param targetFilename
	 * @param newtFilename
	 */
	public static void renameFilename(String targetDir,String targetFilename,String newtFilename) {
		// 対象のパス作成
		File targetFile = createFileObj(targetDir,targetFilename);
		File newFile = createFileObj(targetDir,newtFilename);
		
		// ファイル名変更
		targetFile.renameTo(newFile);
	}

}
