import json
import pickle
import numpy
import os.path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from matplotlib.colors import ListedColormap
from mpl_toolkits.axes_grid import AxesGrid
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText


_CMAP_BWR_LIST = [
	[0.17822806640625, 0.30420105468749997, 0.92985451171875],
	[0.18431333203125, 0.31059705468750004, 0.93020105859375002],
	[0.19039859765625, 0.3169930546875, 0.93054760546875004],
	[0.19648386328125, 0.32338905468750001, 0.93089415234374995],
	[0.20256912890625003, 0.32978505468749997, 0.93124069921875008],
	[0.20865439453125001, 0.33618105468749998, 0.93158724609374999],
	[0.21473966015625001, 0.34257705468749999, 0.93193379296875001],
	[0.22082492578125001, 0.34897305468750001, 0.93228033984375003],
	[0.22691019140625002, 0.35536905468750002, 0.93262688671874994],
	[0.23299545703124999, 0.36176505468749998, 0.93297343359375007],
	[0.23908072265625002, 0.36816105468749999, 0.93331998046874998],
	[0.24516598828125002, 0.3745570546875, 0.93366652734375011],
	[0.25125125390625003, 0.38095305468750001, 0.93401307421875002],
	[0.25733651953125003, 0.38734905468750003, 0.93435962109374993],
	[0.26342178515624998, 0.39374505468750004, 0.93470616796875006],
	[0.26950705078124998, 0.4001410546875, 0.93505271484374997],
	[0.27559231640625004, 0.40653705468750001, 0.9353992617187501],
	[0.28167758203124998, 0.41293305468749997, 0.93574580859375001],
	[0.28776284765624999, 0.41932905468750004, 0.93609235546874991],
	[0.29384811328125005, 0.42572505468749999, 0.93643890234375005],
	[0.29993337890624999, 0.43212105468750001, 0.93678544921874995],
	[0.30601864453125005, 0.43851705468750002, 0.93713199609375009],
	[0.31262257031250001, 0.44451835546875001, 0.93754249218749997],
	[0.31939938281250002, 0.45038808984375001, 0.93797430468750009],
	[0.32617619531249997, 0.45625782421875, 0.9384061171875],
	[0.33295300781250003, 0.46212755859374999, 0.93883792968750002],
	[0.33972982031250004, 0.46799729296874998, 0.93926974218749992],
	[0.34650663281249999, 0.47386702734375002, 0.93970155468750005],
	[0.3532834453125, 0.47973676171875002, 0.94013336718750007],
	[0.36006025781250001, 0.48560649609375001, 0.94056517968749997],
	[0.36683707031250001, 0.49147623046875, 0.94099699218749999],
	[0.37361388281250002, 0.49734596484374999, 0.94142880468750001],
	[0.38039069531249997, 0.50321569921875009, 0.94186061718750003],
	[0.38716750781250003, 0.50908543359375003, 0.94229242968750004],
	[0.39394432031249998, 0.51495516796874996, 0.94272424218749995],
	[0.40072113281249999, 0.52082490234375001, 0.94315605468750008],
	[0.40749794531250005, 0.52669463671874994, 0.94358786718749998],
	[0.41427475781250001, 0.53256437109374999, 0.9440196796875],
	[0.42105157031250001, 0.53843410546874992, 0.94445149218750002],
	[0.42782838281249996, 0.54430383984374997, 0.94488330468750004],
	[0.43460519531250003, 0.55017357421874991, 0.94531511718750005],
	[0.44138200781250003, 0.55604330859375006, 0.94574692968749996],
	[0.44815882031250004, 0.56191304296875, 0.94617874218749998],
	[0.45597787499999998, 0.56844491015624998, 0.94674344531249999],
	[0.46483917187499996, 0.57563891015625002, 0.94744103906249999],
	[0.47370046874999999, 0.58283291015624994, 0.94813863281249999],
	[0.48256176562500003, 0.59002691015625008, 0.9488362265625],
	[0.49142306250000001, 0.59722091015625001, 0.9495338203125],
	[0.50028435937500004, 0.60441491015625004, 0.9502314140625],
	[0.50914565625000008, 0.61160891015624996, 0.9509290078125],
	[0.518006953125, 0.61880291015625, 0.95162660156250001],
	[0.52686825000000004, 0.62599691015625003, 0.95232419531250001],
	[0.53572954687499996, 0.63319091015625006, 0.95302178906250001],
	[0.54459084375, 0.64038491015624999, 0.95371938281249991],
	[0.55345214062500003, 0.64757891015625002, 0.95441697656250002],
	[0.56231343749999996, 0.65477291015625005, 0.95511457031250002],
	[0.57117473437499999, 0.66196691015624998, 0.95581216406249991],
	[0.58003603124999992, 0.66916091015625001, 0.95650975781249992],
	[0.58889732812499995, 0.67635491015625004, 0.95720735156250003],
	[0.5977586250000001, 0.68354891015625008, 0.95790494531250003],
	[0.60661992187500002, 0.69074291015625, 0.95860253906249993],
	[0.61548121875000006, 0.69793691015625003, 0.95930013281249993],
	[0.62434251562499998, 0.70513091015624996, 0.95999772656250004],
	[0.63320381250000002, 0.7123249101562501, 0.96069532031249993],
	[0.64193132812499998, 0.71934652734375004, 0.96142598437499993],
	[0.65025749999999993, 0.72585099609375003, 0.96225585937499991],
	[0.65858367187500011, 0.73235546484375003, 0.96308573437499989],
	[0.66690984375000006, 0.73885993359375002, 0.96391560937499998],
	[0.67523601562500002, 0.74536440234375001, 0.96474548437499996],
	[0.68356218749999997, 0.75186887109375, 0.96557535937499994],
	[0.69188835937500004, 0.75837333984374999, 0.96640523437500003],
	[0.70021453124999999, 0.76487780859374999, 0.96723510937500001],
	[0.70854070312499995, 0.77138227734374998, 0.96806498437499999],
	[0.71686687500000001, 0.77788674609375008, 0.96889485937499997],
	[0.72519304687500008, 0.78439121484374996, 0.96972473437499995],
	[0.73351921875000003, 0.79089568359375007, 0.97055460937499993],
	[0.7418453906250001, 0.79740015234374995, 0.97138448437500002],
	[0.75017156250000006, 0.80390462109375005, 0.972214359375],
	[0.75849773437500001, 0.81040908984374993, 0.97304423437499998],
	[0.76682390624999996, 0.81691355859375003, 0.97387410937500007],
	[0.77515007812500003, 0.82341802734374991, 0.97470398437500005],
	[0.7834762500000001, 0.82992249609375002, 0.97553385937499992],
	[0.79180242187499994, 0.8364269648437499, 0.97636373437500001],
	[0.80012859375000012, 0.84293143359375, 0.97719360937499999],
	[0.80845476562500007, 0.84943590234374999, 0.97802348437499997],
	[0.81678093750000003, 0.85594037109374999, 0.97885335937500006],
	[0.8222050781250001, 0.86026543359375007, 0.97937071874999992],
	[0.82762921875000006, 0.86459049609374994, 0.97988807812500001],
	[0.83305335937500002, 0.86891555859375003, 0.98040543749999998],
	[0.83847749999999999, 0.87324062109375, 0.98092279687500006],
	[0.84390164062500006, 0.87756568359374998, 0.98144015625000003],
	[0.84932578125000002, 0.88189074609374996, 0.981957515625],
	[0.85474992187499998, 0.88621580859375004, 0.98247487499999997],
	[0.86017406250000006, 0.89054087109375002, 0.98299223437499994],
	[0.86559820312500002, 0.89486593359375, 0.98350959375000002],
	[0.87102234374999998, 0.89919099609374997, 0.98402695312499999],
	[0.87644648437500006, 0.90351605859375006, 0.98454431249999996],
	[0.88187062499999991, 0.90784112109374993, 0.98506167187500004],
	[0.88729476562499998, 0.91216618359375001, 0.98557903125000001],
	[0.89271890624999994, 0.91649124609374999, 0.98609639062499999],
	[0.89814304687499991, 0.92081630859375008, 0.98661374999999996],
	[0.90356718749999998, 0.92514137109374994, 0.98713110937499993],
	[0.90899132812499994, 0.92946643359375003, 0.98764846875000001],
	[0.91441546875000002, 0.93379149609375001, 0.98816582812499998],
	[0.91983960937499998, 0.93811655859374998, 0.98868318750000006],
	[0.92526374999999994, 0.94244162109374996, 0.98920054687500003],
	[0.93068789062500001, 0.94676668359375005, 0.98971790624999989],
	[0.93374875781249989, 0.94911941015625001, 0.98696141015625005],
	[0.93602186718749991, 0.95081469140624997, 0.98311362890624998],
	[0.93829497656249994, 0.95250997265624993, 0.97926584765625002],
	[0.94056808593749985, 0.95420525390624999, 0.97541806640624995],
	[0.94284119531249999, 0.95590053515624995, 0.97157028515624999],
	[0.94511430468750002, 0.95759581640625002, 0.96772250390624992],
	[0.94738741406250004, 0.95929109765624998, 0.96387472265625007],
	[0.94966052343749996, 0.96098637890625005, 0.96002694140625],
	[0.95193363281249999, 0.96268166015625001, 0.95617916015624993],
	[0.95420674218750001, 0.96437694140624997, 0.95233137890624997],
	[0.95647985156249993, 0.96607222265625003, 0.9484835976562499],
	[0.95875296093749995, 0.96776750390624999, 0.94463581640624994],
	[0.96102607031249998, 0.96946278515625006, 0.94078803515624998],
	[0.9632991796874999, 0.97115806640625002, 0.93694025390625002],
	[0.96557228906249992, 0.97285334765625009, 0.93309247265624995],
	[0.96784539843749995, 0.97454862890624994, 0.92924469140624999],
	[0.97011850781249997, 0.97624391015625001, 0.92539691015624992],
	[0.97239161718749989, 0.97793919140624996, 0.92154912890624996],
	[0.97466472656249992, 0.97963447265625003, 0.91770134765625],
	[0.97693783593749994, 0.9813297539062501, 0.91385356640625004],
	[0.97921094531249986, 0.98302503515625006, 0.91000578515624997],
	[0.98060742187499994, 0.98398016015625012, 0.90377431640625006],
	[0.98112726562499997, 0.98419512890625005, 0.89515916015624997],
	[0.98164710937499999, 0.98441009765624998, 0.88654400390624999],
	[0.98216695312500002, 0.98462506640625003, 0.87792884765625001],
	[0.98268679687499993, 0.98484003515624996, 0.86931369140624992],
	[0.98320664062499996, 0.98505500390625, 0.86069853515624994],
	[0.98372648437499999, 0.98526997265624994, 0.85208337890624997],
	[0.98424632812500001, 0.98548494140625009, 0.84346822265624999],
	[0.98476617187499993, 0.98569991015625003, 0.83485306640625001],
	[0.98528601562499996, 0.98591487890625007, 0.82623791015625003],
	[0.98580585937499998, 0.98612984765625, 0.81762275390624994],
	[0.98632570312500001, 0.98634481640624994, 0.80900759765625008],
	[0.98684554687499992, 0.98655978515624998, 0.80039244140624999],
	[0.98736539062499995, 0.98677475390625002, 0.7917772851562499],
	[0.98788523437499998, 0.98698972265625007, 0.78316212890625003],
	[0.988405078125, 0.98720469140625, 0.77454697265624994],
	[0.98892492187499992, 0.98741966015625005, 0.76593181640624985],
	[0.98944476562500006, 0.98763462890624998, 0.75731666015624999],
	[0.98996460937499997, 0.98784959765625002, 0.74870150390625001],
	[0.990484453125, 0.98806456640624996, 0.74008634765624992],
	[0.99100429687499991, 0.98827953515625, 0.73147119140624994],
	[0.99136161328125005, 0.98837110546874996, 0.72146517187500003],
	[0.99123134765624998, 0.98809248046874998, 0.70728656249999999],
	[0.99110108203125002, 0.98781385546875, 0.69310795312499995],
	[0.99097081640624995, 0.98753523046875002, 0.67892934374999991],
	[0.99084055078125, 0.98725660546875005, 0.66475073437499999],
	[0.99071028515625004, 0.98697798046875007, 0.65057212499999995],
	[0.99058001953124997, 0.98669935546875009, 0.63639351562499991],
	[0.99044975390625001, 0.98642073046875001, 0.62221490624999998],
	[0.99031948828125005, 0.98614210546875003, 0.60803629687500005],
	[0.99018922265624998, 0.98586348046874994, 0.5938576874999999],
	[0.99005895703125002, 0.98558485546874997, 0.57967907812499997],
	[0.98992869140625006, 0.98530623046874999, 0.56550046875000004],
	[0.98979842578124999, 0.98502760546875001, 0.55132185937499989],
	[0.98966816015625003, 0.98474898046875003, 0.53714324999999996],
	[0.98953789453124996, 0.98447035546875006, 0.52296464062500003],
	[0.98940762890625, 0.98419173046875008, 0.50878603124999999],
	[0.98927736328125004, 0.9839131054687501, 0.49460742187500001],
	[0.98914709765624997, 0.98363448046875002, 0.48042881249999997],
	[0.98901683203125001, 0.98335585546875004, 0.46625020312499998],
	[0.98888656640625006, 0.98307723046875006, 0.45207159374999994],
	[0.98875630078124999, 0.98279860546875009, 0.43789298437500002],
	[0.98862603515625003, 0.98251998046875011, 0.42371437499999998],
	[0.98691322265625003, 0.97674226171875, 0.41706042187499998],
	[0.98520041015624993, 0.97096454296875001, 0.41040646874999998],
	[0.98348759765625005, 0.96518682421875002, 0.40375251562499997],
	[0.98177478515625005, 0.95940910546875002, 0.39709856249999997],
	[0.98006197265625006, 0.95363138671875003, 0.39044460937500003],
	[0.97834916015624995, 0.94785366796875004, 0.38379065625000003],
	[0.97663634765625007, 0.94207594921875004, 0.37713670312499997],
	[0.97492353515625008, 0.93629823046874994, 0.37048274999999997],
	[0.97321072265624997, 0.93052051171875005, 0.36382879687499997],
	[0.97149791015624998, 0.92474279296874995, 0.35717484374999997],
	[0.96978509765624998, 0.91896507421875007, 0.35052089062499997],
	[0.9680722851562501, 0.91318735546874996, 0.34386693749999997],
	[0.96635947265625, 0.90740963671874997, 0.33721298437499997],
	[0.96464666015625, 0.90163191796874997, 0.33055903125000002],
	[0.96293384765625001, 0.89585419921874998, 0.32390507812499997],
	[0.9612210351562499, 0.89007648046874999, 0.31725112499999997],
	[0.95950822265625002, 0.88429876171874999, 0.31059717187499997],
	[0.95779541015625003, 0.87852104296875, 0.30394321874999997],
	[0.95608259765625003, 0.87274332421875001, 0.29728926562499997],
	[0.95436978515624993, 0.86696560546875001, 0.29063531249999996],
	[0.95265697265625005, 0.86118788671875002, 0.28398135937499996],
	[0.95040992578125005, 0.85253234765624997, 0.28085438671875002],
	[0.94798480078124991, 0.84291753515625001, 0.27890307421874999],
	[0.94555967578125, 0.83330272265624994, 0.27695176171874997],
	[0.94313455078124997, 0.82368791015624998, 0.27500044921874994],
	[0.94070942578125005, 0.81407309765624991, 0.27304913671874997],
	[0.93828430078125002, 0.80445828515625006, 0.27109782421875001],
	[0.93585917578125011, 0.79484347265624999, 0.26914651171874998],
	[0.93343405078124997, 0.78522866015625004, 0.26719519921875001],
	[0.93100892578124994, 0.77561384765624997, 0.26524388671874999],
	[0.92858380078125002, 0.76599903515625001, 0.26329257421874996],
	[0.92615867578125, 0.75638422265624994, 0.26134126171875],
	[0.92373355078125008, 0.74676941015624998, 0.25938994921874997],
	[0.92130842578125005, 0.73715459765624991, 0.25743863671875],
	[0.91888330078124991, 0.72753978515625006, 0.25548732421875003],
	[0.91645817578125, 0.71792497265624999, 0.25353601171875001],
	[0.91403305078124997, 0.70831016015625003, 0.25158469921874999],
	[0.91160792578125005, 0.69869534765624997, 0.24963338671874999],
	[0.90918280078125002, 0.68908053515625001, 0.24768207421875002],
	[0.90675767578124999, 0.67946572265624994, 0.24573076171875],
	[0.90433255078124997, 0.66985091015624998, 0.24377944921875003],
	[0.90190742578124994, 0.66023609765625002, 0.24182813671875],
	[0.89962091015625001, 0.65055212109375005, 0.23995634765625001],
	[0.89747300390624996, 0.64079898046875006, 0.23816408203125],
	[0.89532509765625001, 0.63104583984375007, 0.23637181640625002],
	[0.89317719140624996, 0.62129269921874997, 0.23457955078125001],
	[0.89102928515625002, 0.61153955859374998, 0.23278728515625],
	[0.88888137890625007, 0.60178641796874999, 0.23099501953125001],
	[0.88673347265624991, 0.59203327734375, 0.22920275390625],
	[0.88458556640624997, 0.58228013671875001, 0.22741048828125002],
	[0.88243766015624991, 0.57252699609374991, 0.22561822265625001],
	[0.88028975390624997, 0.56277385546875003, 0.22382595703124999],
	[0.87814184765625003, 0.55302071484375004, 0.22203369140624998],
	[0.87599394140624998, 0.54326757421875005, 0.22024142578125],
	[0.87384603515625003, 0.53351443359375006, 0.21844916015625002],
	[0.87169812890624998, 0.52376129296874996, 0.21665689453125],
	[0.86955022265624993, 0.51400815234374997, 0.21486462890624999],
	[0.86740231640624998, 0.50425501171874998, 0.21307236328124998],
	[0.86525441015624993, 0.49450187109374999, 0.21128009765624997],
	[0.86310650390624999, 0.48474873046874994, 0.20948783203125002],
	[0.86095859765625005, 0.47499558984374995, 0.20769556640625],
	[0.85881069140624999, 0.46524244921874996, 0.20590330078124999],
	[0.85666278515624994, 0.45548930859374998, 0.20411103515624998],
	[0.85457037890624998, 0.44447361328125001, 0.2023057734375],
	[0.85264447265624999, 0.42967025390624997, 0.20046152343750001],
	[0.85071856640624999, 0.41486689453125003, 0.19861727343749999],
	[0.84879266015624999, 0.40006353515624998, 0.1967730234375],
	[0.84686675390624999, 0.38526017578124999, 0.19492877343749998],
	[0.84494084765624999, 0.37045681640625, 0.19308452343749999],
	[0.84301494140625, 0.35565345703125001, 0.1912402734375],
	[0.84108903515625, 0.34085009765625002, 0.18939602343750001],
	[0.83916312890624989, 0.32604673828125003, 0.18755177343750001],
	[0.83723722265625, 0.31124337890624998, 0.18570752343749999],
	[0.83531131640624989, 0.29644001953124999, 0.1838632734375],
	[0.83338541015625001, 0.28163666015624994, 0.18201902343749998],
	[0.8314595039062499, 0.26683330078125, 0.18017477343749999],
	[0.82953359765625001, 0.25202994140624996, 0.1783305234375],
	[0.8276076914062499, 0.23722658203124999, 0.17648627343750001],
	[0.82568178515625001, 0.22242322265625, 0.17464202343750002],
	[0.82375587890625002, 0.20761986328125001, 0.1727977734375],
	[0.82182997265625002, 0.19281650390625002, 0.1709535234375],
	[0.81990406640624991, 0.17801314453125, 0.16910927343750001],
	[0.81797816015625002, 0.16320978515625004, 0.16726502343749999],
	[0.81605225390625002, 0.14840642578125002, 0.1654207734375],
	[0.81412634765625003, 0.13360306640625, 0.16357652343750001]
]

_CMAP_BWR = ListedColormap(_CMAP_BWR_LIST, name="BlueWhiteRed")


class Data:

	def __init__(self, format, fields, **kwds):

		if fields is not None:
			for name in kwds:
				if name not in fields:
					raise Exception("Unknown keyword: " + name)

		self.__dict__.update(kwds)
		self.format = format

	def _dump(self, to_python_types=False):

		# forward declaration, to break the vicious cycle
		# of transform() and serializers
		serializers = {}

		def transform(obj):
			t = type(obj)
			if t in serializers:
				return serializers[t](obj)
			else:
				raise ValueError("Cannot serialize values of type " + str(type(obj)))

		serializers.update({
			dict: lambda obj: dict((key, transform(obj[key])) for key in obj),
			list: lambda obj: [transform(elem) for elem in obj],
			numpy.ndarray: lambda obj: obj.tolist(),
			numpy.float32: lambda obj: float(obj),
			numpy.float64: lambda obj: float(obj),
			int: lambda obj: obj,
			float: lambda obj: obj,
			str: lambda obj: obj,
			bool: lambda obj: obj
		})

		data = dict((name, getattr(self, name))
			for name in dir(self) if not name.startswith('_') and
				type(getattr(self, name)) in serializers)

		if to_python_types:
			return transform(data)
		else:
			return data

	def __getattr__(self, name):
		return None

	def save(self, filename, format=None):
		if format is None:
			name, ext = os.path.splitext(filename)
			format = ext[1:]

		if format not in ['pickle', 'json']:
			raise ValueError('Unknown storage format: ' + format)

		to_dump = self._dump(to_python_types=(format == 'json'))

		with open(filename, 'w') as f:
			if format == 'json':
				json.dump(to_dump, f, indent=4)
			else:
				pickle.dump(to_dump, f, protocol=2)

	@classmethod
	def load(cls, filename, format=None):

		all_true = lambda lst, func: reduce(lambda x, y: x and y,
			[func(elem) for elem in lst])

		all_elems_are_lists = lambda lst: all_true(lst,
			lambda elem: isinstance(elem, list))

		all_elems_have_same_length = lambda lst: \
			all_elems_are_lists(lst) and \
			all_true(lst, lambda elem: len(elem) == len(lst[0]))

		all_floats = lambda lst: all_true(lst, lambda elem: isinstance(elem, float))

		def looksLikeNumpyArray(obj):
			if isinstance(obj, list):
				return all_floats(obj) or \
					(all_elems_have_same_length(obj) and
					all_true(obj, lambda elem: looksLikeNumpyArray(elem)))
			else:
				return False

		def transform(obj):
			if isinstance(obj, dict):
				return dict((str(key), transform(obj[key])) for key in obj)
			elif isinstance(obj, list):
				if looksLikeNumpyArray(obj):
					return numpy.array(obj)
				else:
					return obj
			else:
				return obj

		if format is None:
			name, ext = os.path.splitext(filename)
			format = ext[1:]

		if format not in ['pickle', 'json']:
			raise ValueError('Unknown storage format: ' + format)

		with open(filename) as f:
			if format == 'json':
				data = transform(json.load(f))
			else:
				data = pickle.load(f)

		format = data.pop('format')
		return cls._load(format, **data)

	@classmethod
	def _load(cls, format, **kwds):
		return cls(format, kwds.keys(), **kwds)


class XYData(Data):

	def __init__(self, name, xarray, yarray, **kwds):

		assert isinstance(xarray, numpy.ndarray)
		assert isinstance(yarray, numpy.ndarray)
		assert xarray.size == yarray.size

		self.name = name
		self.xarray = xarray
		self.yarray = yarray

		fields = ['ymin', 'ymax', 'xname', 'yname', 'description',
			'source', 'experimental', 'linestyle']
		Data.__init__(self, 'xy', fields, **kwds)

	@classmethod
	def _load(cls, format, **kwds):
		if format != 'xy':
			raise Exception("Wrong data format: " + str(format))
		name = kwds.pop('name')
		xarray = kwds.pop('xarray')
		yarray = kwds.pop('yarray')
		return cls(name, xarray, yarray, **kwds)


class HeightmapData(Data):

	def __init__(self, name, heightmap, **kwds):

		assert isinstance(heightmap, numpy.ndarray)

		self.heightmap = heightmap
		self.name = name

		fields = ['xmin', 'xmax', 'ymin', 'ymax', 'description',
			'source', 'zmin', 'zmax', 'xname', 'yname', 'zname']
		Data.__init__(self, 'heightmap', fields, **kwds)

	@classmethod
	def _load(cls, format, **kwds):
		if format != 'heightmap':
			raise Exception("Wrong data format: " + str(format))
		name = kwds.pop('name')
		heightmap = kwds.pop('heightmap')
		return cls(name, heightmap, **kwds)


class HeightmapPlot:

	def __init__(self, heightmap_data, colorbar=True):
		self.data = heightmap_data

		self.fig = plt.figure()

		subplot = self.fig.add_subplot(111, xlabel=self.data.xname, ylabel=self.data.yname)
		im = subplot.imshow(self.data.heightmap, interpolation='bicubic', origin='lower',
			aspect='auto', extent=(self.data.xmin, self.data.xmax,
			self.data.ymin, self.data.ymax), cmap=_CMAP_BWR,
			vmin=self.data.zmin, vmax=self.data.zmax)

		if colorbar:
			self.fig.colorbar(im, orientation='horizontal', shrink=0.8).set_label(self.data.zname)

	def save(self, filename):
		self.fig.savefig(filename)


class EvolutionPlot:

	def __init__(self, heightmaps_list, shape=None):

		if shape is None:
			shape = heightmaps_list.shape

		self.fig = plt.figure()
		self.grid = AxesGrid(self.fig, 111, nrows_ncols=shape, axes_pad=0.1, label_mode="1", aspect=False)

		for i, e in enumerate(heightmaps_list):
			im = self.grid[i].imshow(e.heightmap, interpolation='bicubic', origin='lower',
				aspect='auto', extent=(e.xmin, e.xmax, e.ymin, e.ymax),
				cmap=_CMAP_BWR, vmin=e.zmin, vmax=e.zmax)

			self.grid[i].text(0, 1, e.name, transform=self.grid[i].transAxes,
				horizontalalignment='left', verticalalignment='top',
				bbox=dict(facecolor='white'), fontsize=6)

			for name in ['left', 'right', 'top', 'bottom']:
				self.grid[i].axis[name].set_visible(False)

		#self.fig.colorbar(im, orientation='horizontal', shrink=0.8)

	def save(self, filename):
		self.fig.savefig(filename)


class XYPlot:

	def __init__(self, xydata_list, legend=True, gradient=False,
		location="lower left", title=None, legendsize='x-small'):

		self.data_list = xydata_list

		# check that data contains the same values
		xname = self.data_list[0].xname
		yname = self.data_list[0].yname
		for data in self.data_list:
			assert data.xname == xname
			assert data.yname == yname

		# find x limits
		xmin = self.data_list[0].xarray[0]
		xmax = self.data_list[0].xarray[-1]
		for data in self.data_list:
			if data.xarray[0] < xmin:
				xmin = data.xarray[0]
			if data.xarray[-1] > xmax:
				xmax = data.xarray[-1]

		# find y limits
		ymin = None
		ymax = None
		for data in self.data_list:
			if data.ymin is not None and (ymin is None or data.ymin < ymin):
				ymin = data.ymin
			if data.ymax is not None and (ymax is None or data.ymax < ymax):
				ymax = data.ymax

		# plot data
		self.fig = plt.figure()

		self.subplot = self.fig.add_subplot(111,
			xlabel=self.data_list[0].xname,
			ylabel=self.data_list[0].yname)

		if not legend:
			colors = ["0.2"] * len(self.data_list)
		else:
			colors = [None] * len(self.data_list)

		if gradient:
			l = len(self.data_list)
			colors = [(float(i) / (l - 1), 0, 1.0 - float(i) / (l - 1)) for i in xrange(l)]

		for i, data in enumerate(self.data_list):
			kwds = {'label': data.name}
			if colors[i] is not None:
				kwds['color'] = colors[i]
			if data.linestyle is not None:
				kwds['linestyle'] = data.linestyle

			self.subplot.plot(data.xarray, data.yarray,
				('o' if data.experimental else '-'), **kwds)

		self.subplot.set_xlim(xmin=xmin, xmax=xmax)
		self.subplot.set_ylim(ymin=ymin, ymax=ymax)

		if legend:
			self.subplot.legend(loc=location, prop={'size': legendsize})

		if title is not None:
			self.subplot.set_title(title)

		self.subplot.grid(True)

	def save(self, filename, xmin=None, xmax=None, ymin=None, ymax=None):
		self.subplot.set_xlim(xmin=xmin, xmax=xmax)
		self.subplot.set_ylim(ymin=ymin, ymax=ymax)
		self.fig.savefig(filename)
