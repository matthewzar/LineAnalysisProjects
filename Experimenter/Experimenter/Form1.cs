using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Timers;
using System.Windows.Forms;
using Experimenter;
using Experimenter.AccessorTesting;

namespace Experimenter
{

    public partial class Form1 : Form
    {
        #region

        public Form1()
        {
            InitializeComponent();
        }

        #endregion

        private void btnTestClick_Click(object sender, EventArgs e)
        {
            var person = new Person();

            Console.WriteLine(person.SSN);
            person.SSN = "123";
            Console.WriteLine(person.SSN);
            person.SSN = "12341234123412";
            Console.WriteLine(person.SSN);
            person.SSN = null;
            Console.WriteLine(person.SSN);

            MessageBox.Show("Hello world");
            Console.WriteLine("Step 2");
        }

        private int _sum(List<int> things)
        {
            int ret = 0;
            foreach (var val in things)
            {
                ret += val * 2;
            }
            return ret;
        }
    }
}