import os
import md5

"""
    Generates a new repository-addons.xml file from each addons addon.xml file,
    a new addons.xml.md5 hash file and the new zip.md5 files. Must be run from
    the root of the checked-out repo. Only handles single depth folder structure.
"""

def save_file(data, file):
    try:
        # Write data to the file
        open(file, "w").write(data)
    except Exception, e:
        # Error when writting the file
        print "An error occurred saving %s file!\n%s" % (file, e)

def generate_addons_file(folder, file):
    # Addon list
    addons = os.listdir(folder)
    
    # Inicial addon xml file text
    addons_xml = u"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<addons>\n"
   	
    # Loop thru and copy each addons addon.xml file
    for addon in addons:
        try:
            # Create path to the addon
            path = os.path.join(folder, addon)

            # Skip files and .svn or .git folders
            if (not os.path.isdir(path) or addon == ".svn" or addon == ".git"): continue

            # Create path of the file
            path = os.path.join(path, "addon.xml")
            
            # Split lines for stripping
            xml_lines = open(path, "r").read().splitlines()
            
            # New Addon
            addon_xml = ""

            # Loop thru cleaning each line
            for line in xml_lines:
                # Skip encoding format line
                if (line.find("<?xml" ) >= 0): continue
                # Add line
                addon_xml += unicode(line.rstrip() + "\n", "UTF-8")
            
            # We succeeded so add to our final addons.xml text
            addons_xml += addon_xml.rstrip() + "\n\n"
        except Exception, e:
            # Missing or poorly formatted addon.xml
            print "Excluding %s for %s" % (path, e)
    # Clean and add closing tag
    addons_xml = addons_xml.strip() + u"\n</addons>\n"
    
    # Save file
    save_file(addons_xml.encode("UTF-8"), file)

def generate_addons_zip_md5(folder):
    # Addon list
    addons = os.listdir(folder)

    # Loop thru and generate zip MD5
    for addon in addons:
        try:
            # Create path of the addon
            path = os.path.join(folder, addon)

            # Skip files and .svn or .git folders
            if (not os.path.isdir(path) or addon == ".svn" or addon == ".git"): continue

            # Find files in addon directory
            files = os.listdir(path)
            for f in files:
                types = f.split(".")

                # Find zip files in addon directory
                if(types[len(types)-1] == "zip"):
                    # Create path of the file
                    path = os.path.join(path, f)
                    # Generate MD5 of zip file
                    generate_md5_file(path)
        except Exception, e:
            # Error on creating zip MD5
            print "Excluding because %s" % (e)

def generate_md5_file(file):
    try:
        # Create a new MD5 hash
        m = md5.new(open(file).read()).hexdigest()
        # Save file
        file = file + ".md5"
        save_file(m, file)
    except Exception, e:
        # Error when generating MD5 file
        print "An error occurred creating %s file!\n%s" % (file, e)

if (__name__ == "__main__"):
    repository = "pischkou-addons.xml"
    addons_dir = "zips"
    generate_addons_file(addons_dir, repository)
    generate_md5_file(repository)
    generate_addons_zip_md5(addons_dir)

    print "Finished Updating Addons XML and MD5 Files"