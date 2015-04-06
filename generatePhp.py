import numpy

class generatePhp():
    def saveAsPhp(self, phpfile, data):
        # Open output file and write headers.
        outfile = self.createphpfile(phpfile)

        # Write PHP header
        outfile = self.createphpheader(outfile)

        outfile.write('<table class="colormap" align="center" width=85%% border=1>\n')
        # Body
        for count,row in enumerate(data):
                outfile.write('<tr>\n')
                outfile.write('  <td>\n')
                outfile.write('      <div class="row">%i</div>' % count)
                outfile.write('  </td>\n')
                for col in row:
                    red, green, blue = col
                    outfile.write('  <td bgcolor="#%s%s%s">\n' % (hex(red)[-2:], hex(green)[-2:], hex(blue)[-2:]))
                    outfile.write('  </td>\n')
                outfile.write('</tr>\n')
        outfile.write('</table>\n\n')

        # Footer
        self.closephpfile(outfile)
        return

    def createphpheader(self, outfile):
        # createphpheader: Prep php file with php header
        phpstr = """
        <?php
            date_default_timezone_set('America/Los_Angeles');
        ?>"""

        outfile.write('%s\n' % phpstr)
        outfile.write('<br />\n')
        return outfile
    
    def createphpfile(self, phpfile):
        # Create an php output file with a stylesheet header. Returns file id
        # used by fprintf.
        outfile = open(phpfile,'w')
        outfile.write('<html>\n')
        headstr = """<link rel="stylesheet" href="colormap.css" title="colormap-css" media="all" type="text/css">"""
            
        outfile.write('%s\n' % headstr)
        outfile.write('<br />\n<body>\n')
        return outfile

    def closephpfile(self, outfile):
        outfile.write('</body>\n</html>\n')
        outfile.close()
        return