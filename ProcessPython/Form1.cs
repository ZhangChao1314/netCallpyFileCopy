using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using GeneralTool.General.ProcessHelpers;

namespace ProcessPython
{
    public partial class Form1 : Form
    {
        ProcessServer server;
        public Form1()
        {
            InitializeComponent();
            server = new ProcessServer();
            server.ErrorHandler += Server_ErrorHandler;
            server.Exited += Server_Exited;
            server.ReceivedHandler += Server_ReceivedHandler;            
        }

        private void 启动pyToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //读取python文件
            var open = new OpenFileDialog();
            
            DirectoryInfo exePath = new DirectoryInfo(Environment.CurrentDirectory);// 应用程序所在目录，即bin/debug
            string pythonpath = exePath.Parent.Parent.FullName;//上2级目录
            open.InitialDirectory = pythonpath;//设置打开路径的目录
            open.Filter = "py|*.py";
            if (open.ShowDialog() != DialogResult.OK)
            {
                return;
            }
            //执行python文件
            string path1 = "D:\\C#\\netCallpyFileCopy\\ProcessPython\\test.xlsx";//自己的excel文件路径
        
            string args0 = $" {open.FileName} --action 1";
            string args1 = $" {open.FileName} {path1}";
            string args2 = $" {open.FileName} {2} {3}";           
            string pyexePath = @"C:\Users\zhang\.conda\envs\mypython37\python.exe";//VS2022中用conda创建的python37环境
            string pyexePath1 = @"C:\ProgramData\Anaconda3\python.exe";//当前默认python
            string pyexePath2 = @"C:\Program Files(x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe";//VS2022自己安装的python
            
            //server.Run("python", args0);//选MiLoser​的 main.py文件时，运行代码
            server.Run("python", args1);//选我自己的test.py文件时，运行的代码
            //server.Run(pyexePath, args2);//选武林大皮虾​main0.py文件时，运行的代码
            //目前的Run无任何返回值，如只需要返回值，建议python代码中不要有任何print代码，
            //只有最后return参数，main中一定要用print来返回到C#代码中

        }

        private void Server_ReceivedHandler(object sender, string e)
        {
            this.AddLog(e);
        }

        private void Server_Exited(object sender, EventArgs e)
        {
            this.AddLog("Python process exit");
        }

        private void Server_ErrorHandler(object sender, string e)
        {
            if (string.IsNullOrWhiteSpace(e))
            {
                return;
            }
            this.AddLog(e);
        }

        private void button1_Click(object sender, EventArgs e)
        {
            //this.server.WriteMessage(this.textBox1.Text);
        }


        private void AddLog(string v)
        {
            this.Invoke(new Action(() =>
            {
                this.richTextBox1.AppendText(v + Environment.NewLine);
            }));

        }


    }
}
