ip="172.16.1.122"

mountFolder="/home/yoctoadm/Desktop/netFolder/"

rs_od="//hiodwsfsvs01.hbi.ad.harman.com/Toyota_CY17_MEU/"
rs_bu="//hirowsfsvs01.ad.harman.com/TOYOTA/Toyota_CY17_MEU/"
rs_mu="//himuwsfsvs01.ad.harman.com/TOYOTA/Toyota_CY17_MEU/"
rs_na="//hingwssccm02.ad.harman.com/TOYOTA/"
rs_ch="//hicgwsfsvs01.hbi.ad.harman.com/TOYOTA/Toyota_CY17_MEU/"

echo $rs_od

sudo mount.cifs $rs_od $mountFolder -o user="SKalinina",pass="Harman/0588",dom="ADHARMAN",rw


#sudo umount netFolder/