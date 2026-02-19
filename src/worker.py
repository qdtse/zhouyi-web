from workers import WorkerEntrypoint, Response
import json

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        url = request.url
        method = request.method
        
        # CORS headers
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Content-Type": "application/json"
        }
        
        # Handle OPTIONS for CORS
        if method == "OPTIONS":
            return Response.new_response(None, status=204, headers=headers)
        
        # Health check
        if url.path in ["/health", "/api/health"]:
            return Response.new_json({"status": "ok"}, headers=headers)
        
        # API routes
        if method == "POST":
            try:
                body = await request.json()
            except:
                return Response.new_json({"error": "Invalid JSON"}, status=400, headers=headers)
            
            # Divine text
            if url.path in ["/divine/text", "/api/divine/text"]:
                result = self._divine_text(body)
                return Response.new_json(result, headers=headers)
            
            # Divine zhuge
            if url.path in ["/divine/zhuge", "/api/divine/zhuge"]:
                result = self._divine_zhuge(body)
                return Response.new_json(result, headers=headers)
            
            # Divine pair
            if url.path in ["/divine/pair", "/api/divine/pair"]:
                result = self._divine_pair(body)
                return Response.new_json(result, headers=headers)
            
            # Divine ziwei
            if url.path in ["/divine/ziwei", "/api/divine/ziwei"]:
                result = self._divine_ziwei(body)
                return Response.new_json(result, headers=headers)
            
            # Divine bazi
            if url.path in ["/divine/bazi", "/api/divine/bazi"]:
                result = self._divine_bazi(body)
                return Response.new_json(result, headers=headers)
            
            # Divine match
            if url.path in ["/divine/match", "/api/divine/match"]:
                result = self._divine_match(body)
                return Response.new_json(result, headers=headers)
        
        # Random divination
        if url.path in ["/divine/random", "/api/divine/random"]:
            result = self._divine_random()
            return Response.new_json(result, headers=headers)
        
        # Current time divination
        if url.path in ["/divine/current", "/api/divine/current"]:
            result = self._divine_current()
            return Response.new_json(result, headers=headers)
        
        # 404
        return Response.new_json({"error": "Not found"}, status=404, headers=headers)
    
    def _divine_text(self, body):
        text = body.get("text", "")
        focus = body.get("focus", "general")
        from api import utils
        return utils.calculate_hexagram_from_text(text, focus)
    
    def _divine_zhuge(self, body):
        text = body.get("text", "")
        from api import utils
        return utils.calculate_zhuge_from_text(text)
    
    def _divine_pair(self, body):
        num1 = body.get("num1", 0)
        num2 = body.get("num2", 0)
        from api import utils
        return utils.calculate_hexagram_from_numbers(num1, num2)
    
    def _divine_random(self):
        from api import utils
        return utils.get_random_divination()
    
    def _divine_current(self):
        from api import utils
        return utils.get_current_time_divination()
    
    def _divine_ziwei(self, body):
        year = body.get("year", 1990)
        month = body.get("month", 1)
        day = body.get("day", 1)
        hour = body.get("hour", 12)
        from api import ziwei
        chart = ziwei.ZiweiChart(year, month, day, hour)
        return chart.json()
    
    def _divine_bazi(self, body):
        year = body.get("year", 1990)
        month = body.get("month", 1)
        day = body.get("day", 1)
        hour = body.get("hour", 12)
        from api import bazi
        return bazi.get_bazi_analysis(year, month, day, hour)
    
    def _divine_match(self, body):
        from api import bazi
        male = bazi.get_bazi_analysis(
            body.get("male_year", 1990),
            body.get("male_month", 1),
            body.get("male_day", 1),
            body.get("male_hour", 12)
        )
        female = bazi.get_bazi_analysis(
            body.get("female_year", 1990),
            body.get("female_month", 1),
            body.get("female_day", 1),
            body.get("female_hour", 12)
        )
        return bazi.check_marriage_compatibility(male, female)
