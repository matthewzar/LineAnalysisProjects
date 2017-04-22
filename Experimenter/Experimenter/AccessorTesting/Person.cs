using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Experimenter.AccessorTesting
{
    class Person
    {
        private string DeepDarkSecret;
        public string NickName;


        public string Name { get; private set; }
        //This code is what happens in the background when writing a partial property like the one above
//      private string _name;
//      public string Name
//      {
//          get { return _name; }
//          private set { _name = value; }
//      }


        //private field for storing string data associated with the public SSN property
        private string _ssn = "00000000000000";
        public string SSN
        {
            get { return "****"+ _ssn.Substring(4); }
            /*private*/ set
            {
                if (value == null)
                {
                    throw new ArgumentNullException("SSN can't be null"); 
                }

                if (string.IsNullOrWhiteSpace(value) || value.Length != 14)
                { return; }
                _ssn = value;
            }
        }
    }
}