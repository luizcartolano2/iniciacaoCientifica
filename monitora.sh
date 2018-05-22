#!/bin/bash

#Atualizado em 13/11/2017
#Script para verificar se determinados processos estao em execucao
#Dar permissao
#chmod 777 monitora.sh &
#Executar com nohup
#nohup ./monitora.sh &

#Verifica se o arquivo temporario existe e o remove.
if [ -e /tmp/procluiz.tmp ]; then
rm /tmp/procluiz.tmp
fi
#Check em cada 10m
INTERVALO=600
#Define os documentos que pretende monitorar
PROCESSOS=("tweets_cp.py" "getRoutesGoogleMaps_campinas.py" "weatherCampinas.py")
while true; do
   #Executa para cada processo passado como par  metro.
   for i in "${PROCESSOS[@]}"; do

      #Executa o comando ps para todos os usu  rios e filtra com o grep o processo monitorado, depois s  o executados filtros inversos para excluir
      #aparicoees da execucao do proprio grep e do nosso script. O resultado, se existir,sera salvo em um arquivo temporario.
      ps aux | grep "$i" | grep -v "grep" | grep -v "monitora.sh" > /tmp/procluiz.tmp

      #Calcula-se o n  mero de linhas do arquivo criado acima e atribui esse valor    vari  vel A.
      A=$(wc -l /tmp/procluiz.tmp | awk '{print $1}')

      #Se A    maior ou igual a 1 significa que o processo esta  em execucao,
      #entao    salva uma linha contendo um OK para o processo monitorado naquele momento.
      #Sen  o    salvo um ERRO no log e temb  m    enviado um email para o administrador do sistema avisando do ocorrido.
      if [ $A -ge 1 ]; then
         echo -e "$i\tOK\t$(date +"%x\t%X")" >> /local1/luiz/monitora/processos.log
         #$(date +%Y)/$(date +%m)/$(date +%d).log
      else
         if [ "$i" == "python tweets_cp.py" ]; then
            cd /local1/luiz/tweets/
            nohup python tweets_cp.py &
         elif [ "$i" == "python getRoutesGoogleMaps_campinas.py" ]; then
            cd /local1/luiz/routes/
            nohup python getRoutesGoogleMaps_campinas.py &
         elif [ "$i" == "python weatherCampinas.py" ]; then
            cd /local1/luiz/weather/
            nohup python weatherCampinas.py &
        fi
         echo -e "$i\tERRO\t$(date +"%x\t%X")" >> /local1/luiz/monitora/processos.log
         #$(date +%Y)/$(date +%m)/$(date +%d)
         #echo -e "\nPor algum motivo inesperado o processo $i n  o est   sendo executado neste momento." | mutt -s "[ALERTA] Problemas com $i em $(date +"%x  %X")" francessantos@lrc.ic.unicamp.br -a  /t$
      fi
   done
   sleep $INTERVALO
done
