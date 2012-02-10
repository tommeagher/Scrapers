#1/usr/bin/env python
from mechanize import Browser
from BeautifulSoup import BeautifulSoup

outfile = open("artscraper.txt", "w")

mech = Browser()
url = "http://www.jerseyarts.com/OnlineGuide.aspx?searchType=advanced&searchTerm=D%3ad7%3bR%3ar1%2cr2%2cr3%2cr4%3bSp%3a0%3bGc%3a0%3bF%3a0"
page = mech.open(url)

html = page.read()
soup = BeautifulSoup(html)

for row in soup.findAll('table', {"class" : "GuideResultInfoWrapper"}):
    name = row.find('div', {"class" : "GuideResultListingName"}).a.string
    street = row.find('div', {"class" : "GuideResultAddress"}).span.string
    city = street.findNext('span').string
    record = (name, street, city)
    print >> outfile, "; ".join(record)

outfile.close()


# a sample of the html structure of the website
#                        <div id="ctl00_wpmSiteWide_gwpGuideSearchResults1_GuideSearchResults1_rptSearchResults_ctl01_pnlOrgInfo" class="GuideResultAlternateRow">
#                         <table cellpadding="0" cellspacing="0" border="0" class="GuideResultInfoWrapper">
#                          <tr>
#                           <td style="text-align:center;width:113px;">
#                            <a id="ctl00_wpmSiteWide_gwpGuideSearchResults1_GuideSearchResults1_rptSearchResults_ctl01_lnkGuideDetailFromImage" title='View details for "Artists&squot; Gallery"' href="GuideDetail.aspx?listingID=665dd1b1-7386-4479-aa10-d9073108afa5">
##                             <img id="ctl00_wpmSiteWide_gwpGuideSearchResults1_GuideSearchResults1_rptSearchResults_ctl01_imgOrgImage" src="FileHandlers/orgImageThumb.ashx?listingID=665dd1b1-7386-4479-aa10-d9073108afa5" style="border-width:0px;" />
 #                           </a>
 #                          </td>
 #                          <td>
  #                          <div class="GuideResultListingName">
   ##                          Artists' Gallery
   #                          </a>
   #                         </div>
#                            <div class="GuideResultAddress">
#                             <span id="ctl00_wpmSiteWide_gwpGuideSearchResults1_GuideSearchResults1_rptSearchResults_ctl01_lblAddress">
##                              18 Bridge Street
 #                            </span>
 #                            <br />
 #                            <span id="ctl00_wpmSiteWide_gwpGuideSearchResults1_GuideSearchResults1_rptSearchResults_ctl01_lblCitySateZip">
 #                             Lambertville, NJ 08530
 #                            </span>
 #                           </div>
 ##                           <div>
  #                           <span id="ctl00_wpmSiteWide_gwpGuideSearchResults1_GuideSearchResults1_rptSearchResults_ctl01_lblDescription">
  #                            <span id="ctl00_wpmSiteWide_gwpGuideSearchResults1_GuideSearchResults1_rptSearchResults_ctl01_lblDescription" class="GuideResultDescription">
  #                             Artists' Gallery is a partnership of eighteen professional visual artists who cooperatively administer, staff and exhibit
  ##                             <a href="GuideDetail.aspx?listingID=665dd1b1-7386-4479-aa10-d9073108afa5" title="View Event Details">
  #                              ...more
  #                             </a>
  #                            </span>
  #                           </span>
  #                          </div>
  #                         </td>
  #                         <td align="right" valign="top">
  #                         </td>
  #                        </tr>
  #                       </table>
   #                     </div>
