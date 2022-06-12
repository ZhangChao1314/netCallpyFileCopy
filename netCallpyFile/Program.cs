using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace netCallpyFile
{
    class Program
    {
        static void Main(string[] args)
        {
            string[] strArr = new string[2];//参数列表
            string sArguments = @"main.py";//这里是python的文件名字
            strArr[0] = "2";
            strArr[1] = "3";
            RunPythonScript(sArguments, "-u", strArr);

        }

        //调用python核心代码
        public static void RunPythonScript(string sArgName, string args = "", params string[] teps)
        {
            Process p = new Process();
            string path = System.AppDomain.CurrentDomain.SetupInformation.ApplicationBase + sArgName;// 获得python文件的绝对路径（将文件放在c#的debug文件夹中可以这样操作）
            //path = @"C:\Users\19239\Desktop\test\" + sArgName;//(因为我没放debug下，所以直接写的绝对路径,替换掉上面的路径了)
            //p.StartInfo.FileName = @"C:\Users\zhang\.conda\envs\mypython37\python.exe";//(注意：用的话需要换成自己的)没有配环境变量的话，可以像我这样写python.exe的绝对路径(用的话需要换成自己的)。如果配了，直接写"python.exe"即可
            p.StartInfo.FileName = @"C:\ProgramData\Anaconda3\python.exe";
            string sArguments = path;
            foreach (string sigstr in teps)
            {
                sArguments += " " + sigstr;//传递参数
            }

            sArguments += " " + args;

            p.StartInfo.Arguments = sArguments;

            p.StartInfo.UseShellExecute = false;

            p.StartInfo.RedirectStandardOutput = true;

            p.StartInfo.RedirectStandardInput = true;

            p.StartInfo.RedirectStandardError = true;

            p.StartInfo.CreateNoWindow = true;

            p.Start();
            p.BeginOutputReadLine();
            p.OutputDataReceived += new DataReceivedEventHandler(p_OutputDataReceived);
            Console.ReadLine();
            p.WaitForExit();
        }
        //输出打印的信息
        static void p_OutputDataReceived(object sender, DataReceivedEventArgs e)
        {
            if (!string.IsNullOrEmpty(e.Data))
            {
                Console.WriteLine(e.Data + Environment.NewLine);
            }

        }
    }
}
