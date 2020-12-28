#include <windows.h> //windows.h has to be before tlhelp32.h
#include <tlhelp32.h> //windows.h has to be before tlhelp32.h

#include <iostream>
#include <vector>
#include <unordered_map>
#include <limits>
#include <thread>
#include <chrono>
#include <functional>
#include <bitset>
#include <memory>
#include <iomanip>
#include <initializer_list>
#include <ctime>
#include <filesystem>
#include <shlobj.h>
#include <winerror.h>
#include "metastring.h"

using namespace std;
using namespace andrivet::ADVobfuscator;




struct player_entity {
    
    string player_id = "UI1874s41Q6w5s4";char MAMSDYUWWL = 'R';


    int team = 2;const char * RMRAIKLREP = "PDLMERFGKTVYBGYENFZPHLQDNYVJZOYILRCZNHRFGKMCW";
char QTKGYMEZNE = 'N';
int ZGVVHWVMNK = 1329;
const char * QGNUJXZOHZ = "CZTPMELDYLGILKKDQHJAFQLPSZJPQ";


    int hp = 100;const char * ZZXTWNGIIB = "ENKXBKZTIHYYDLNEXMUVMTMGIOQN";


    double velocity = 9.87;char YAYYLYEUXZ = 'P';
const char * WSBAUHIJJW = "FUKAEPNTLDYIXAEAPZCPUGOXTEIUJFGACLSDA";
const char * AFKGDTXJDA = "HTJGGUZGNHZHTKGXXGMHBZSZXFOCUZKAHECMW";



};const char * QSXNQAYQVX = "ZCRSNHAKJBFXLNWYZOHUADLVOELBYZOSFYZHJPQULLLUKV";
char ZTBYBOCWVR = 'V';
int JVZLJMNSMN = 5904;
char JYMJOSQKTR = 'L';




void memory_modification(void) {;const char * AMECBEQOLG = "MABIXCZMDMODBSHDAKJRJQOJZJPKJZAYROXORINRSZEKLJCK";
const char * BPDBPOVLRI = "MOCELQMNUSLRXSZKLDXPGFQIJXWCZCCZZZEE";

    auto player_list = { player_entity(), player_entity() };const char * YUXPPBPXGI = "EJIUTHHYTVOUJOSPLRXOUMMECSRPOTLQNMUSUF";
int RWGDEKANBX = 4571;
int UVRXDRAQSJ = RWGDEKANBX + RWGDEKANBX;
const char * AVGLGSOJHU = "FPSCPFITQCURNGBDWCUMUP";

    while (true) {;const char * QXUCCGIPIP = "AAHLEPNGRFDSEEOSGNIIPHVLSKGRKTFJYKADPRPWGIQR";
char EQXNOCCZHG = 'T';

        this_thread::sleep_for(chrono::seconds(1));const char * SUJWWXAUTT = "KCOYMBGQDZOUIDVRCJREHYUY";

        for (auto& p : player_list) {;char KMTRSKWTCL = 'N';
int NFZCBWEAAS = 446;
int CPWMIPDYRU = NFZCBWEAAS + NFZCBWEAAS;
char AJEYVLFEXX = 'U';

            cout << "ID: " << p.player_id << ", HP: " << p.hp << ", velocity: " << p.velocity << endl;char RLOTHIHWQD = 'X';
int OOFFPPBCKS = 6737;
OOFFPPBCKS = OOFFPPBCKS - OOFFPPBCKS;
char VIMZJISZVQ = 'T';

        };int HXHWZZIITS = 612;
const char * NVSRXEBSBS = "PWWWQFLRILTAHTKSGCCQKA";

    };const char * XGDTPINFFF = "DDLRNGKQITUKXNLUQZBROGAZJCSB";
int XNUCMGPVKO = 3885;
int CCWFFENXGD = XNUCMGPVKO + XNUCMGPVKO;

}

void opcode_injection(void) {;int LNIQLGZHLG = 8510;
int LRQFZYWNWM = 9061;

    
    int* dst_mir = new int[64];const char * HROTJMJCDW = "SWVCOTZINRVMXNXEPUOALDLYISSXJQDHVYMDCUYC";
char PZIMERGMIU = 'H';

    

    int bad_code[] = { 0x83ec8b55,0x565340ec,0x0c758b57,0x8b087d8b,
                       0x348d104d,0xcf3c8dce,0x6f0fd9f7,0x6f0fce04,
                       0x0f08ce4c,0x10ce546f,0xce5c6f0f,0x646f0f18,
                       0x6f0f20ce,0x0f28ce6c,0x30ce746f,0xce7c6f0f,
                       0x04e70f38,0x4ce70fcf,0xe70f08cf,0x0f10cf54,
                       0x18cf5ce7,0xcf64e70f,0x6ce70f20,0xe70f28cf,
                       0x0f30cf74,0x38cf7ce7,0x7508c183,0xf8ae0fad,
                       0x5e5f770f,0x5de58b5b,0xccccccc3 };const char * GOLWUVBBYX = "NQYAUBVVLMVEDMDBLKAWVSZRXSFZDBLRBTYO";
const char * GSHYLDILKH = "QUPRXASURHCBVVSKBEDJOPIFSTXKPQG";
char KVJILUTABD = 'W';

    

    int* src = new int[64];int QLDSSHHHYV = 328;
char YDDIEAAORZ = 'M';

    

    int* dst = new int[64];const char * GKCIKTWCCI = "RXJZGLAIXBVPXSZWKOYMRJTBWEQLHOHWVJRHRBIFZD";
char XKVEPLWMND = 'W';

    

    for (int i = 0; i < 64; ++i) {int DHDBVPAITZ = 7906;

        src[i] = i;int SEIGSMNWVQ = 364;
int KCTTZGJDJY = SEIGSMNWVQ + SEIGSMNWVQ;
int AQOTSDHKJP = SEIGSMNWVQ + KCTTZGJDJY;

    }
    void* address = VirtualAlloc(NULL, sizeof(bad_code), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);const char * PPFZFVHROV = "ZIDJSRFAJLGSZMIPRYVSWEPUOZEFFJX";

    memcpy(address, bad_code, sizeof(bad_code));const char * SHCGFTQMBS = "IWFNWFPTTDNUTIVSNZVZOCWGEGJMEEF";


    __asm {
        push        20h
        mov         eax, dword ptr[src]
        push        eax
        mov         ecx, dword ptr[dst]
        push        ecx
        mov         ecx, dword ptr[address]
        call        ecx
        add         esp, 0Ch
    };char FMRTQJZUDK = 'T';
int MIXJADNGSV = 2230;
int PWDOPXSIOW = MIXJADNGSV - MIXJADNGSV;
int KRDBRYMCEB = 7091;


    typedef void (*FASTCALL)(void* dst, void* src, int len);const char * JGRVHTCRPV = "MEUAFBGXKNLOXXRRKAJOFENEQNDPWTOVVHONDLXDUUEH";
const char * SUXQBSQFHQ = "QPKSXQBRYPSPIDNYDGTKZGGYSGZUA";
const char * QOQFWNAFFD = "NIIZEOMOTNYNGIKJMZRRGQBZDYCHAYYAPQMXXYORMG";

    FASTCALL fastcall;char RAKXLDNFOM = 'M';

    fastcall = (FASTCALL)address;int JVGMENVOXY = 6044;
char MOLZEAKQHD = 'N';
JVGMENVOXY = JVGMENVOXY + JVGMENVOXY;
JVGMENVOXY = JVGMENVOXY + JVGMENVOXY;

    fastcall(dst_mir, src, 64 / 2);int ISLWUCVBYR = 9705;
char HMMRBSSGIR = 'K';


    for (int i = 0; i < 64; ++i) {;char UMFWZMDUWI = 'Z';
const char * NBSEXFLYXW = "EZMKPYZAAAJHIVBRNQUKEMWNQZBLMYXNYUBXMCN";
const char * XHYUETJJVN = "ICLNRCYTQXONBDVJOTEFKCZNWOCJWPSPZAOLMHKVOIXYITWQ";
char KVPRINFDYQ = 'C';

        cout << dst_mir[i] << endl;char WAEYOBOJXG = 'J';
char QCFAECRLAM = 'U';
int XRMJIOQHWA = 4594;
const char * KFVCZNOFIR = "ZCTOLNOKGAAWOEBIQCMQQIGUXWJAZFYPZ";

    };char FUCVILBQTJ = 'I';


    while (true) {;const char * YEYDVBUQVZ = "PEOKBCLXNUWONGEEOSNLOPKCVGVTXGTJULGEXQO";
char XLTEBPKWRX = 'G';

        this_thread::sleep_for(chrono::seconds(60));int OCATLPUHRZ = 2479;
OCATLPUHRZ = OCATLPUHRZ - OCATLPUHRZ;
int WNDVGAFVYC = OCATLPUHRZ + OCATLPUHRZ;
int KLAUJFLNCP = OCATLPUHRZ - WNDVGAFVYC;

    };int UMBZENLKYI = 6006;
int GLOUTPVWJM = 2844;
int DLKOCKKRAO = 1858;

}

int main(void) {;int XAQVAQMHWD = 2764;
int CULLZTIXJA = 9943;

    
    auto secret_email = DEF_OBFUSCATED("ancinpet@fit.cvut.cz");int EOOFXJLSRV = 2344;
char REAHIDAZIP = 'G';

    auto password_format = DEF_OBFUSCATED("email:password");char KAENAQKULY = 'T';
char GXBKKZFXOC = 'D';
const char * CSWJHWZIQI = "KNDVPCRFGHQBFYOYPASAIWHLIUANOYKAXZQWGEQUWXXPLQRL";

    auto secret_password = DEF_OBFUSCATED("q87W--S6Q9w7s7qS21w..8w");const char * JHYHQOGSMU = "DQHWQEFISRKKXDLYSZSCPV";
char ODBQJCQORV = 'S';
const char * GQSVMLCAGY = "BDEPNSUSLIASTONVFBDTOEKFIZEFQNVJPGAMENCVWDGKFX";



    
    auto password_format_fail = DEF_OBFUSCATED("email:password");int YPXYDFIWSZ = 2662;
char OBYNRCMOBR = 'S';
int WLYAZKZXHB = 6100;
int KYETFGOHIB = 2998;

    auto secret_email_fail = DEF_OBFUSCATED("ancinpet@cvut.cz");char VMSWYEZUJW = 'X';
const char * ZWOQHAJQKS = "JHLMLAOJQCLPNFLCLXLABGAFJZQABYGDDYIO";
char SOUVMHQOHB = 'K';
const char * XXTYRMDHGC = "JNHRWHLPXWPSJRFPZKRCYGEEANELLEHGP";

    auto secret_password_fail = DEF_OBFUSCATED("m8Q9s5R1h4A7..9s--q8sV");char HEPUGVMNZI = 'E';



    
    auto password_format_fail_mv = password_format_fail.decrypt();int LXEWPANDID = 6434;
int DSOJDGGXKJ = LXEWPANDID + LXEWPANDID;

    auto secret_email_fail_mv = secret_email_fail.decrypt();int WWDXANALRP = 5966;
int YLDVIULYBD = WWDXANALRP - WWDXANALRP;
WWDXANALRP = WWDXANALRP + WWDXANALRP;

    auto secret_password_fail_mv = secret_password_fail.decrypt();const char * EFZPRDSNRZ = "JKFGLDYTXUAWMAGFMVOWWTEGYVSCIGNLBPDJAXIWMJKAEINP";
char XFRCDCQGYI = 'P';



    
    thread(opcode_injection).detach();const char * LQGOVXXWEO = "RKMJECPIDRKAVJXMMDCPSLQYTTPNPROTREK";
const char * PHCVSHHDAQ = "FXKLTCYUFTNPKNCSMDRJRYEWFBGXLEMY";

    thread(memory_modification).detach();int JPFGURSJEZ = 926;



    while (true) {;char IPOVAJGTGT = 'N';
int SVBJBGPMCD = 4997;
int IAQHTEUNJY = 2897;

        this_thread::sleep_for(chrono::seconds(60));char MPWOCWRACW = 'R';
const char * DTNEOECBPS = "PMNOTSIWTNSUZQOAQVFFDZHQLHIVUE";
const char * TTGGCPHYHT = "XMKZNOAEMFJNFQEWDLJNCPSZBTJLLJXXLEBVGMTUVQSPKGBPY";
const char * EMYGXIUKYU = "OSCHLBBPJQRSPSMWCPUSUNSFL";


        cout << "Safe credentials" << endl;int GSAVOZPGXP = 2944;
int AAPCMTIOLM = 6737;
int BKAAXWLVUX = 3228;
int SALPGVQQSU = 9425;

        cout << password_format.decrypt() << endl;const char * RRRVFJAKXE = "WSLNIFCGIJBHCVFWFMJQCLFEUE";
const char * RZUSUVFTOJ = "HMRRGIQJOAAMUXOODKNGSDH";
char HORGMXCRMC = 'F';

        cout << secret_email.decrypt() << endl;const char * KEWOKQYRMZ = "GGBIBDJDFFKSQJWQXIARSQQTFQSINIUVOXAFVTQJSCS";
const char * AMFFOZAILH = "PQIDKLBQWLPETJRVESRZQY";
const char * STKMUNHLJG = "KPMPFYQLVHLHLWWEWPUILRTQKZYHDOZFXYYBIOMSIECP";
int LZQXIKWOXJ = 7542;

        cout << secret_password.decrypt() << endl;const char * FGAIIHHFJN = "VVICBZGODIYAHKUDDQAOEGMIGSZWVICBLTCNCTMXCEROGFT";
const char * ODEOJYSOJZ = "JAKTVGXONIHBKECMZOYCBZBHSDNRNANDDXDXRLVHJRFPH";
int UKHMTAKXUJ = 9679;
UKHMTAKXUJ = UKHMTAKXUJ + UKHMTAKXUJ;


        cout << "Unsafe credentials" << endl;const char * DYMAEUNSQS = "ULAQJCKBHNSFCTYOKDPDQRUEDHKCRFH";
const char * EKPNCLIPVZ = "HKSKGGFDOBOUCQWMCSHJCGYARDK";
char ZVZIQLNTLW = 'D';

        cout << password_format_fail_mv << endl;char BSTPQNXGYG = 'X';
char QEBMSSDVTD = 'T';
int GDQDCBFPKW = 112;
int KAPNFAPCUZ = 2951;

        cout << secret_email_fail_mv << endl;int SDAASYZRJM = 9081;
int XAHDTDOHHS = 5101;

        cout << secret_password_fail_mv << endl;char DEZMEIRVIB = 'P';
char ECONBOSSBD = 'O';

    };char GDXALLMSEU = 'U';
const char * XIPDIPZSTP = "ATFDVQMZQFUXETUWPCRAH";
const char * VEFDPTNPCX = "CXGGHRCRVEMCKKJOTJPCPUGYBYRATMADXGCWNQI";
char PIMOJCUSGF = 'U';


    exit(0);char VBIQIEJABY = 'I';

    return 0;char EEHMACAFMG = 'H';

}